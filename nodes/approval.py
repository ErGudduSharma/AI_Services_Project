"""
Approval Node: Final decision-making logic based on validation results.
"""

def approval_node(state):
    """
    Updates the 'approved' status of the workflow based on prior validation.
    """
    # Logic: Successfully validated requests are automatically approved
    if state.get('validated'):
        state['approved'] = True 
    else:
        state['approved'] = False 
        
    return state 