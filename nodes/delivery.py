def delivery_node(state):
    if state['approved']:
        state['result'] = "Workflow completed successfully"
    else:
        state['result'] = "Workflow rejected during approval"
    return state 