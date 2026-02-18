"""
Approval Node: Final decision-making logic based on validation results.

"""

def approval_node(state):
    """
    Updates the 'approved' status of the workflow based on prior validation.
    
    """
    # Simple Logic: Agar validation successful tha, toh automatically approve kar do
    if state.get('validated'):
        state['approved'] = True # Haan
    else:
        state['approved'] = False # Naa
        
    return state 