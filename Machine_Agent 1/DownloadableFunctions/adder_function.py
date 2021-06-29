
def introduction():
    function_type = 'addition_function'
    dependant_functions = []
    active_passive = 'passive'
    performative_types = ['request_to_add']
    return {'function_type': function_type, 'Dependant Function': dependant_functions, "active_passive": active_passive,
            "performative_types": performative_types}


def execute(inputs):
    inputs = eval(inputs)
    a = inputs[0]
    b = inputs[1]
    return add(a,b)



def add(a,b):
    return a+b