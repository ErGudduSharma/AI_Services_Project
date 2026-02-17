"""
Data Fetch Node: Extracts business entities from unstructured user input.
"""
from llm.gemini_client import get_gemini_llm
import json
import re

def data_fetch_node(state):
    """
    Uses a hybrid approach of Regular Expressions (Regex) and AI (Gemini)
    to extract Customer ID, Amount, and Status.
    """
    request_text = state['client_request']
    
    # --- PHASE 1: Deterministic Extraction (Regex) ---
    # This acts as a safety layer if the AI service is unavailable.
    id_pattern = r'ID[:\s]+([A-Za-z0-9-]+)'
    amt_pattern = r'(\d+[\d,.]*)'
    
    id_match = re.search(id_pattern, request_text, re.IGNORECASE)
    amount_match = re.search(amt_pattern, request_text)
    
    # Initialize data with identified entities or defaults
    extracted_id = id_match.group(1) if id_match else "Unknown"
    extracted_amount = 0
    
    if amount_match:
        try:
            # Clean number string (remove commas) and convert to float
            clean_amt = amount_match.group(1).replace(',', '')
            extracted_amount = float(clean_amt)
        except ValueError:
            extracted_amount = 0

    state['data'] = {
        "customer_id": extracted_id,
        "amount": extracted_amount,
        "status": "PENDING"
    }

    # --- PHASE 2: Intelligent Enhancement (Gemini AI) ---
    try:
        llm = get_gemini_llm()
        prompt = f"""
        Extract the following as JSON from this text: customer_id, amount, status.
        Text: {request_text}
        
        Return ONLY valid JSON. Keep amount as a number.
        """
        response = llm.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            # Extract JSON block using regex from the AI response
            json_block = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_block:
                ai_extracted = json.loads(json_block.group(0))
                
                # Merge AI findings with existing data if they are better
                if ai_extracted.get('customer_id') and ai_extracted['customer_id'] != "Unknown":
                    state['data']['customer_id'] = ai_extracted['customer_id']
                
                if ai_extracted.get('amount'):
                    try:
                        state['data']['amount'] = float(ai_extracted['amount'])
                    except:
                        pass
                        
    except Exception as e:
        # We don't fail the workflow here because we already have the Regex fallback data.
        state['error'] = f"Data Module: Enhanced extraction bypassed. (Reason: {str(e)})"
    
    return state 