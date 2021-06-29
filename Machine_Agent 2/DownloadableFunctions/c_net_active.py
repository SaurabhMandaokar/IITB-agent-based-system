import time
from BaseLibraries.conversationStarters import conversation_starter

def introduction():
    function_type = 'generate_cfp_for_transport'
    dependant_functions = []
    active_passive = 'active'
    performative_types = ['cfp_for_transport', "cfp_for_transport_cost"]
    return {'function_type': function_type, 'Dependant Function': dependant_functions, "active_passive": active_passive,
            "performative_types": performative_types}


def active(msg_to_send_queue):
    print("active_function c-net-active is activated on a thread")
    while True:

        time.sleep(15)
        protocol = 'contract_net_interaction_protocol'
        performative = 'call_for_proposal'
        performative_type = 'cfp_for_transport'
        content = "[1,10]"
        conversation_starter(protocol, performative, performative_type, content,msg_to_send_queue)

    return

