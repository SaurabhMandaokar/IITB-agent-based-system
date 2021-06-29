def introduction():
    function_type = 'responce_to_proposals'
    dependant_functions = []
    active_passive = 'passive'
    performative_types = ['proposals_for_transport', "proposals_for_transport_cost"]
    return {'function_type': function_type, 'Dependant Function': dependant_functions, "active_passive": active_passive,
            "performative_types": performative_types}


def execute(performative_type,all_proposals):
    senders, costs = [],[]
    for message in all_proposals:
        senders.append(message.sender)
        costs.append(message.content)
    max_cost_index = costs.index(max(costs))
    accept_proposal = senders[max_cost_index]

    return accept_proposal

