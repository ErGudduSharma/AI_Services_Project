from llm.gemini_client import get_gemini_llm
import json

def data_fetch_node(state):
    try:
        llm = get_gemini_llm()
        prompt = f"""
        Extract the following information from this business request as JSON:
        - customer_id (if not found, use 'Unknown')
        - amount (extract as a number, ignore currency symbols, default to 0 if not found)
        - status (default to 'PENDING')
        
        Request: {state['client_request']}
        
        IMPORTANT: Return ONLY valid JSON and nothing else.
        """
        response = llm.generate_content(prompt)
        # Clean response text in case of markdown blocks
        clean_text = response.text.replace('```json', '').replace('```', '').replace('json', '').strip()
        state['data'] = json.loads(clean_text)
    except Exception as e:
        # Fallback if AI extraction fails
        state['data'] = {
            "customer_id": "Extraction Failed",
            "amount": 0,
            "status": "ERROR"
        }
        state['error'] = f"Data fetch failed: {str(e)}"
    
    return state 