def validation_node(state):
    try:
        data = state.get('data', {}) 
        amount = data.get('amount', 0)

        # Basic risk rule: anything under 100,000 is auto-validated
        if isinstance(amount, (int, float)) and amount < 100000:
            state['validated'] = True 
        else:
            state['validated'] = False 
    except Exception as e:
        state['validated'] = False
        state['error'] = f"Validation failed: {str(e)}"
        
    return state 
