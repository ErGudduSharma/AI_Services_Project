"""
Data Fetch Node: Extracts business entities from unstructured user input.
"""
from llm.gemini_client import get_gemini_llm # Gemini model lana
import json # JSON data handle karne ke liye
import re # Regex use karke text se pattern dhundne ke liye

def data_fetch_node(state):
    """
    Uses a hybrid approach of Regular Expressions (Regex) and AI (Gemini)
    to extract Customer ID, Amount, and Status.
    """
    request_text = state['client_request'] # User ka original message
    
    # --- PHASE 1: Deterministic Extraction (Regex) ---
    # Ye code base extraction hai jo AI ke bina bhi kaam karega
    id_pattern = r'ID[:\s]+([A-Za-z0-9-]+)' # ID dhundne ka pattern
    amt_pattern = r'(\d+[\d,.]*)' # Amount dhundne ka pattern (paisa)
    
    id_match = re.search(id_pattern, request_text, re.IGNORECASE)
    amount_match = re.search(amt_pattern, request_text)
    
    # Agar pattern mil gaya toh extract karo, warna default 'Unknown' ya 0 rakho
    extracted_id = id_match.group(1) if id_match else "Unknown"
    extracted_amount = 0
    
    if amount_match:
        try:
            # Amount mein se comma hatakar use number (float) mein badlo
            clean_amt = amount_match.group(1).replace(',', '')
            extracted_amount = float(clean_amt)

        except ValueError:
            extracted_amount = 0

    # Initial data state mein save kiya
    state['data'] = {
        "customer_id": extracted_id,
        "amount": extracted_amount,
        "status": "PENDING" # Shuruat mein hamesha PENDING hoga
    }

    # --- PHASE 2: Intelligent Enhancement (Gemini AI) ---
    # Ab AI se puchenge taaki behtar extraction ho sake
    try:
        llm = get_gemini_llm()
        # AI ko instruction: Text se customer_id, amount, status khinch kar JSON mein do
        prompt = f"""
        Extract the following as JSON from this text: customer_id, amount, status.
        Text: {request_text}
        
        Return ONLY valid JSON. Keep amount as a number.
        """
        response = llm.generate_content(prompt)
        
        if response and hasattr(response, 'text') and response.text:
            
            # AI ke response mein se JSON block dhundo
            json_block = re.search(r'\{.*\}', response.text, re.DOTALL)

            if json_block:
                ai_extracted = json.loads(json_block.group(0))
                
                # Agar AI ne behtar ID dhundi hai toh Regex wale data ko overwrite (merge) karo
                if ai_extracted.get('customer_id') and ai_extracted['customer_id'] != "Unknown":
                    state['data']['customer_id'] = ai_extracted['customer_id']
                
                # Amount ko bhi refine kiya
                if ai_extracted.get('amount'):
                    try:
                        state['data']['amount'] = float(ai_extracted['amount'])
                    except:
                        pass
                        
    except Exception as e:
        # Agar AI fail hota hai toh process nahi rokna, kyunki Regex se pehle hi data nikal chuke hain
        state['error'] = f"Data Module: Enhanced extraction bypassed. (Reason: {str(e)})"
    
    return state # Update ki hui state vapas return ki
