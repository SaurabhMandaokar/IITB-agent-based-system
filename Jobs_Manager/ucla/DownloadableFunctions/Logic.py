#PASSIVE

import os

# function_pointing_table={}
# function_pointing_table_file = open(r"C:\Users\Saourabh\PycharmProjects\phase2\anik files\Agent\\FunctionPointingConfig.txt")
# function_pointing_table_file_contents = function_pointing_table_file.read()
# Lines = function_pointing_table_file_contents.splitlines()
# for line in Lines:
#     key_values=line.split("=>")
#     key=key_values[0]
#     value=(key_values[1]).split("|")
#     function_pointing_table[key] = value
#
# ##print(function_pointing_table['Logic'])
#
# dependancy_list=function_pointing_table['Logic']
# for element in dependancy_list:
#     key,value=element.split("->")
#     if key == 'CBM':
#         string='import AgentFunctions.'+value+' as CBM'
#         exec(string)
#     elif key == 'Single Machine Sequencing':
#         string='import AgentFunctions.'+value+' as SingleMachineSequencing'
#         exec(string)
#     elif key == 'BasicMathOperation':
#         string='import AgentFunctions.'+value+' as BasicMathOperation'
#         exec(string)
#


def introduction():
    function_type = 'Logic'
    dependant_functions = ['CBM', 'Single Machine Sequencing', 'BasicMathOperation']
    active_passive = 'passive'
    return {'function_type': function_type, 'Dependant Function': dependant_functions, 'active_passive': active_passive}




