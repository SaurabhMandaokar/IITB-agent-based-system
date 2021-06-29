import random


def introduction():
    function_type = 'transport_cost'
    dependant_functions = []
    active_passive = 'passive'
    performative_types = ['cfp_for_transport', "cfp_for_transport_cost"]
    return {'function_type': function_type, 'Dependant Function': dependant_functions, "active_passive": active_passive,
            "performative_types": performative_types}


def execute(performative_type,inputs):
    inputs = eval(inputs)
    a = inputs[0]
    b = inputs[1]
    return random.randint(a, b)

