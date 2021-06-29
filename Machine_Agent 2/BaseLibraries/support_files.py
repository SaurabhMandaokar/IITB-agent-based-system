import json
import os
import importlib.util
import threading

from BaseLibraries.messaging import FIPA_message
# 1. iterate over each functions introduction at start of agent
# 2. key will be performative_type and value will be function_type
# 3. there is additional function type to function mapping text file that user can edit
#    this file is read it is the function_pointing text file
# ---------------------------------------------------------------------------------------
# type to function_type mapping creator (at start of agent)
        # create a file
        # read intro
        # map type to function type


# There is a need of function pointing generator (at start of agent)
        # read each intro
        # for each function type (key) these function name (values) are to be added in text file

# the below function creates both mapping as well as pointing text files
from DownloadableFunctions import Single_Machine_Sequencing_Considering_Maintenace_Action

folder_location = r'C:\Users\Saourabh\PycharmProjects\phase2\AgentFunctions'


def create_mapping_and_pointing_files(paths_dictionary,msg_to_send_queue):

    # creating files for mapping and pointing at start of agent
    folder_path = paths_dictionary['agent_functions_path']
    mapping = open("type_to_function_mapping.txt", "w+")
    pointing = open("function_pointing.txt", "w+")

    # recognizing which active functions to start using the config file
    # config file exists, and is not created when agent starts
    active_fn_flags = {}
    active_fns_file = open(paths_dictionary['active_functions_configuration'],'r')
    config_file_contents = active_fns_file.read()
    Lines = config_file_contents.splitlines()
    for line in Lines:
        key_values = line.split("=>")
        key = key_values[0]
        values = key_values[1]
        active_fn_flags[key] = values

    # initials for creating an agent file
    agent_file_data = {}
    agent_file_data['agent_name'] = paths_dictionary['agent_name']
    agent_file_data['agent_role'] = paths_dictionary['agent_role']

    filenames = os.listdir(folder_path) # filenames in folder of active and passive functions
    current_performative_types = []
    active_responce_list, passive_responce_list = [],[]
    dict_pointer = {}
    for filename in filenames:
        if filename[-3:] == '.py':
            filepath = os.path.join(folder_path, filename)
            spec = importlib.util.spec_from_file_location(filename, filepath)
            python_script = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(python_script)
            func_intro = python_script.introduction()
            # now func_intro has dictionary returned by the individual module in AgentFunctions
            print('reading ',filename)
            if func_intro['active_passive'] == 'passive':
                # creating performative_type to function_type mapping
                try:
                    for prf_typ in func_intro['performative_types']:
                        passive_responce_list.append(prf_typ)
                        if prf_typ not in current_performative_types:
                            mapping.write(f"{prf_typ}=>{func_intro['function_type']}\n")
                            current_performative_types.append(prf_typ)
                except:
                    print(f"{filename} does not have performative_type")

                # adding available pointer fuctions (.py filenames) to function types
                # for each function type (key) these function name (values) are to be added in text file

                curr_fn_typ = func_intro['function_type']
                if curr_fn_typ not in dict_pointer:
                    # [1] is given to the first function recognized in the function_type
                    dict_pointer[curr_fn_typ] = f"{filename[:-3]}[1]"
                else:
                    current_value = dict_pointer[curr_fn_typ]
                    # other functions recognized for same function_type are given [0] as preference
                    # the pointing file is made such that 0 and 1 value are editable by user
                    new_value = f"{current_value}|{filename[:-3]}[0]"
                    dict_pointer[curr_fn_typ] = new_value

            elif func_intro['active_passive'] == 'active':
                for prf_typ in func_intro['performative_types']:
                    active_responce_list.append(prf_typ)
                if active_fn_flags[filename[:-3]] in ['1', 1]:
                    (threading.Thread(target = python_script.active, args = [msg_to_send_queue,])).start()

    for key in dict_pointer:
        pointing.write(f"{key}=>{dict_pointer[key]}\n")

    for prf_typ in active_responce_list:
        agent_file_data[prf_typ] = {'send': 1, 'receive': 0}
    for prf_typ in passive_responce_list:
        if prf_typ not in active_responce_list:
            agent_file_data[prf_typ] = {'send': 0, 'receive': 1}
        else:
            agent_file_data[prf_typ] = {'send': 1, 'receive': 1}
    agent_nickname = paths_dictionary['agent_name']
    with open(f"{agent_nickname}.json", "w+") as json_file:
        json.dump(agent_file_data, json_file)
    json_file.close()
    mapping.close()
    pointing.close()
    active_fns_file.close()

    return


# reading type to function mapping
    # read type to function mapping txt
    # see key = type and get value = function type
    # return function type string
def map_performative_type(performative_type):

    mapping_table = {}
    mapping_file = open("type_to_function_mapping.txt", "r")
    mapping_file_contents = mapping_file.read()
    Lines = mapping_file_contents.splitlines()

    for line in Lines:
        key_values = line.split("=>")
        key = key_values[0]
        values = key_values[1]
        mapping_table[key] = values
    required_value = mapping_table[performative_type]
    return required_value


# the below part is reading... function_type to fuction mapping (or) function pointing
# this should return target function name as string
# =============================================================================

def pointing(function_type):
    function_pointing_table={}
    function_pointing_file = open("function_pointing.txt","r")
    function_pointing_file_contents = function_pointing_file.read()
    Lines = function_pointing_file_contents.splitlines()

    for line in Lines:
        key_values=line.split("=>")
        key=key_values[0]
        values=(key_values[1]).split("|")
        function_pointing_table[key] = values

    required_values = function_pointing_table[function_type]

    for value in required_values:
        if value[-3:] == '[1]':
            return value[:-3]

    return

# =========================================================================
# the final part is execution of that function and generating an output


def function_execution(function_name,performative_type,inputs,paths_dictionary):  # filename is actually the .py file
    folder_location = paths_dictionary['agent_functions_path']
    filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
    for filename in filenames:
        print(function_name,filename[:-3])
        if filename[-3:] == '.py' and filename[:-3] == function_name:
            filepath = os.path.join(folder_location, filename)
            spec = importlib.util.spec_from_file_location(filename, filepath)
            python_script = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(python_script)
            execution_result = python_script.execute(performative_type,inputs)

            print(execution_result)
            return execution_result

    print('executable function file not found in downloadable functions')
    return


def create_a_reply_to_send(message,reply_parameters):

    if reply_parameters:
        reply = FIPA_message()
        reply.performative = reply_parameters["reply_performative"]
        reply.type = reply_parameters["reply_type"]
        reply.content = reply_parameters["reply_content"]
        reply.receiver = message.sender
        reply.protocol = message.protocol
        reply.conversation_id = message.conversation_id
        return reply


def map_and_point(message):
    performative_type = message.type
    function_category = map_performative_type(performative_type)
    executable_function_name = pointing(function_category)
    if executable_function_name:
        return executable_function_name
    else:
        return None


