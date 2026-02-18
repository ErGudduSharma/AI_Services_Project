"""
Planner Node: Analyzes user requests and generates logical steps for the workflow.
"""
from llm.gemini_client import get_gemini_llm # Gemini model ko khichne wala function

def planner_node(state):
    """
    Predicts the list of business steps needed based on the client input.
    If the AI service is busy or restricted, it provides a high-quality fallback plan.
    """
    try: 
        llm = get_gemini_llm() # AI model initialize kiya

        # AI ko instruction di ki client ki request ko steps mein break kro
        prompt = f"""Break this business request into a list of logical workflow steps: {state['client_request']}
        Return only the list of steps, one per line."""

        response = llm.generate_content(prompt) # AI se reply maanga
        
        # check if response is not empty and has text attribute
        if response and hasattr(response, 'text') and response.text:
            # AI ke response ko clean karke ek list banayi
            steps = [s.strip('- ').strip() for s in response.text.split("\n") if s.strip()]
            # Agar steps mil gaye toh state mein update kiya, warna default steps rakhe
            state['plan'] = steps if steps else ['Analyze requirements', 'Extract data', 'Execute security check']
        else:
            raise Exception("Empty AI response text")

    except Exception as e: 
        # Agar AI down hai toh ye default plan follow karega process rokne ke bajaye
        state['plan'] = [
            'Preliminary Requirement Analysis', 
            'Identity & Parameters Extraction', 
            'Policy Compliance & Shield Validation', 
            'Final Solution Synthesis'
        ]
        # Error message bhi save kiya taaki baad mein pata chale fallback kyu hua
        state['error'] = f"Planning Module: Falling back to template (Service busy: {str(e)})" 

    return state 