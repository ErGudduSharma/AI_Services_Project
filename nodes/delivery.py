from llm.gemini_client import get_gemini_llm

def delivery_node(state):
    try:
        if state.get('approved'):
            llm = get_gemini_llm()
            prompt = f"""
            Based on the following workflow results, provide a detailed, professional solution summary for the user.
            User Request: {state['client_request']}
            Data Extracted: {state['data']}
            Plan Followed: {state['plan']}
            
            Format it as a friendly response. Include what was done and the final outcome.
            """
            response = llm.generate_content(prompt)
            state['result'] = response.text if response and response.text else "Workflow completed successfully."
        else:
            state['result'] = "We are sorry, but your request could not be approved based on our validation rules (e.g., amount limit exceeded)."
    except Exception as e:
        state['result'] = f"Workflow finished with an error in delivery: {str(e)}"
        
    return state 