"""
Planner Node: Analyzes user requests and generates logical steps for the workflow.
"""
from llm.gemini_client import get_gemini_llm 

def planner_node(state):
    """
    Predicts the list of business steps needed based on the client input.
    If the AI service is busy or restricted, it provides a high-quality fallback plan.
    """
    try: 
        llm = get_gemini_llm() 
        prompt = f"""Break this business request into a list of logical workflow steps: {state['client_request']}
        Return only the list of steps, one per line."""
        response = llm.generate_content(prompt) 
        
        if response and hasattr(response, 'text') and response.text:
            # Clean and filter the response to get a clean list of steps
            steps = [s.strip('- ').strip() for s in response.text.split("\n") if s.strip()]
            state['plan'] = steps if steps else ['Analyze requirements', 'Extract data', 'Execute security check']
        else:
            raise Exception("Empty AI response text")

    except Exception as e: 
        # Standard fallback plan to ensure the workflow proceeds even during AI downtime
        state['plan'] = [
            'Preliminary Requirement Analysis', 
            'Identity & Parameters Extraction', 
            'Policy Compliance & Shield Validation', 
            'Final Solution Synthesis'
        ]
        state['error'] = f"Planning Module: Falling back to template (Service busy: {str(e)})" 

    return state 