from llm.gemini_client import get_gemini_llm 

def planner_node(state):
    try: 
        llm = get_gemini_llm() 
        prompt = f"""Break this business request into a list of logical workflow steps: {state['client_request']}
        Return only the list of steps, one per line."""
        response = llm.generate_content(prompt) 
        
        if response and hasattr(response, 'text') and response.text:
            # Filter empty lines and cleaning
            steps = [s.strip('- ').strip() for s in response.text.split("\n") if s.strip()]
            state['plan'] = steps if steps else ['Analyze requirements']
        else:
            state['plan'] = ['Initial Review']

    except Exception as e: 
        state['plan'] = ['Planning Fallback']
        state['error'] = f"Planning error: {str(e)}" 

    return state 