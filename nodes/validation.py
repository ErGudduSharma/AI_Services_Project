"""
Validation Node: Performs deterministic business rule checks on extracted data.
"""

def validation_node(state):
    """
    Applies logic to validate the request parameters.
    Default Rule: Amount must be less than 100,000 for automatic validation.
    """
    try:
        data = state.get('data', {}) 
        amount = data.get('amount', 0)

        # Ensure amount is a numeric type before comparison
        if isinstance(amount, (int, float)) and amount < 100000:
            state['validated'] = True 
        else:
            state['validated'] = False 
            
    except Exception as e:
        state['validated'] = False
        state['error'] = f"Validation Module Failure: {str(e)}"
        
    return state 
