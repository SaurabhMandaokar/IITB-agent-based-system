
def introduction():
    function_type = 'BasicMathOperation'
    dependant_functions = []
    active_passive = 'Passive'
    return {'Function Type':function_type,'Dependant Function':dependant_functions, 'active_passive' : active_passive}

def mul(a,b):
    return a*b

def div(a,b):
    if b!=0:
        return a/b
    else:
        return float('inf')

