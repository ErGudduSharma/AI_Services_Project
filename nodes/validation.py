"""
Validation Node: Performs deterministic business rule checks on extracted data.
"""

def validation_node(state):
    """
    Applies logic to validate the request parameters.
    Default Rule: Amount must be less than 100,000 for automatic validation.
    """
    try:
        data = state.get('data', {}) # Extracted data khichna
        amount = data.get('amount', 0) # Amount check karna

        # Rule check: Agar amount number hai aur 1 lakh se kam hai
        if isinstance(amount, (int, float)) and amount < 100000:
            state['validated'] = True # Toh pass (True)
        else:
            state['validated'] = False # Toh fail (False)
            
    except Exception as e:
        state['validated'] = False # Error aane par fail maano
        state['error'] = f"Validation Module Failure: {str(e)}"
        
    return state # Result vapas dena 
