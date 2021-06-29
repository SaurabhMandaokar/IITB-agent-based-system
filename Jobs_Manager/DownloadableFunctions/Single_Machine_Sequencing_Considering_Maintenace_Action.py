# PASSIVE

import os
import pickle
import datetime
import pandas as pd
from BaseLibraries.conversationStarters import conversation_starter

function_pointing_table = {}
function_pointing_table_file = open("FunctionPointingConfig.txt")
function_pointing_table_file_contents = function_pointing_table_file.read()
Lines = function_pointing_table_file_contents.splitlines()
for line in Lines:
    key_values = line.split("=>")
    key = key_values[0]
    value = (key_values[1]).split("|")
    function_pointing_table[key] = value

dependancy_list = function_pointing_table['Single_Machine_Sequencing_Considering_Maintenace_Action']
for element in dependancy_list:
    key, value = element.split("->")
    if key == 'Machine Condition Monitoring':
        string = 'import DownloadableFunctions.' + value + ' as MachineConditionMonitoring'
        exec(string)
    elif key == 'Single Machine Sequencing':
        string = 'import DownloadableFunctions.' + value + ' as SingleMachineSequencing'
        exec(string)


####################################################################################
def introduction():
    function_type = 'Single Machine Sequencing with Maintenance Consideration'
    dependant_functions = ['Machine Condition Monitoring', 'Single Machine Sequencing']
    active_passive = 'passive'
    performative_types = ['cfp_for_new_job_arrival', 'cfp_for_job_of_failed_machine', 'request_pi_change',
                          'request_di_change', 'accepted_job_proposal']
    return {'function_type': function_type, 'dependant_functions': dependant_functions,
            'active_passive': active_passive, 'performative_types': performative_types}


####################################################################################
def new_job_arrival_penalty(new_job_data):
    data = SingleMachineSequencing.current_queue()
    maintenance_schedule = MachineConditionMonitoring.callable()
    if maintenance_schedule['maintenance action'] != 'NA':
        maintenance_job_data = [maintenance_schedule['maintenance action'], maintenance_schedule['maintenance time'],
                                maintenance_schedule['maintenance date'], 0, float('inf')]
        row_number = len(data)
        data.loc[row_number] = maintenance_job_data
    row_number = len(data)
    data.loc[row_number] = new_job_data
    # print(data)
    data['Di'] = pd.to_datetime(data['Di'])
    data['Di'] = (data['Di'] - pd.Timestamp.now().normalize()).dt.days
    # print(data)
    penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
    return (penalty_optimal_seq_data['penalty'])


####################################################################################
def pi_change(job_data):
    data = SingleMachineSequencing.current_queue()
    # print(data)
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        return 'Job is not in the queue'
    else:
        data.loc[row_location[0]] = job_data
        if 'success' == SingleMachineSequencing.update_current_queue(data):
            # print(data)
            penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
            optimal_queue = penalty_optimal_seq_data['optimal queue']
            # print(optimal_queue)
            if 'success' == SingleMachineSequencing.update_optimal_queue(optimal_queue):
                return 'success'
            else:
                return 'error'
        else:
            return 'error'


####################################################################################
def di_change(job_data):
    data = SingleMachineSequencing.current_queue()
    # print(data)
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        return 'Job is not in the queue'
    else:
        data.loc[row_location[0]] = job_data
        if 'success' == SingleMachineSequencing.update_current_queue(data):
            # print(data)
            penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
            optimal_queue = penalty_optimal_seq_data['optimal queue']
            # print(optimal_queue)
            if 'success' == SingleMachineSequencing.update_optimal_queue(optimal_queue):
                return 'success'
            else:
                return 'error'
        else:
            return 'error'


# ###################################################################################
def job_assignment(job_data):
    data = SingleMachineSequencing.current_queue()
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        row_number = len(data)
        data.loc[row_number] = job_data
        SingleMachineSequencing.update_current_queue(data)
        maintenance_schedule = MachineConditionMonitoring.callable()
        if maintenance_schedule['maintenance action'] != 'NA':
            maintenance_job_data = [maintenance_schedule['maintenance action'],
                                    maintenance_schedule['maintenance time'], maintenance_schedule['maintenance date'],
                                    0, float('inf')]
            row_number = len(data)
            data.loc[row_number] = maintenance_job_data
        print(data)
        data['Di'] = pd.to_datetime(data['Di'])
        data['Di'] = (data['Di'] - pd.Timestamp.now().normalize()).dt.days
        print(data)
        penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
        optimal_queue = penalty_optimal_seq_data['optimal queue']
        print(optimal_queue)
        if SingleMachineSequencing.update_optimal_queue(optimal_queue) == 'success':
            return 'success'
        else:
            return 'error'
    else:
        return 'Job is already in the queue'


####################################################################################
def machine_fail(time_for_maintenace):
    pd.options.mode.chained_assignment = None

    penalty_threshold_file = open(
        "DataBase\\Single_Machine_Sequencing_Considering_Maintenace_Action\\penalty_threshold.txt")
    penalty_threshold = float(penalty_threshold_file.read())

    data = SingleMachineSequencing.current_queue()
    # print(data)

    data['Di'] = pd.to_datetime(data['Di'])
    data['Di'] = (data['Di'] - pd.Timestamp.now().normalize()).dt.days
    # print(data)
    data['Di'] = data['Di'] - time_for_maintenace
    # print(data)

    job_to_bid = data[data.Di < 1]
    # print(job_to_bid)
    data = pd.concat([data, job_to_bid]).drop_duplicates(keep=False)
    # print(data)

    penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
    penalty = penalty_optimal_seq_data['penalty']
    # print(penalty)
    while (penalty > penalty_threshold):
        penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
        optimal_queue = penalty_optimal_seq_data['optimal queue']
        # print(optimal_queue)
        job_to_bid = pd.concat([data[data.Ji == optimal_queue[0]], job_to_bid])
        data = data[data.Ji != optimal_queue[0]]
        # print(data)
        penalty_optimal_seq_data = SingleMachineSequencing.penalty_and_optimal_sequence(data)
        penalty = penalty_optimal_seq_data['penalty']
        # print(penalty)

    # print(job_to_bid)
    for i in range(len(job_to_bid['Di'])):
        days_in_column = job_to_bid['Di'][i]
        days_in_column = int(days_in_column)
        job_to_bid['Di'][i] = (
                datetime.date.today() + datetime.timedelta(days=time_for_maintenace + days_in_column)).strftime(
            "%m-%d-%Y")

        protocol = 'contract_net_interaction_protocol'
        performative = 'call_for_proposal'
        performative_type = 'cfp_for_job_of_failed_machine'
        content = []
        conversation_starter(protocol, performative, performative_type, content)

    print(job_to_bid)

    if 'success' == SingleMachineSequencing.update_current_queue(data):
        return 'success'
    else:
        return 'error'


####################################################################################
def execute(performative_type, content):
    if performative_type == 'cfp_for_new_job_arrival' or performative_type == 'cfp_for_job_of_failed_machine':
        output_performative_type = 'propose_penalty'
        output_result = new_job_arrival_penalty(content)
        comments = None
    elif performative_type == 'request_pi_change':
        function_output = pi_change(content)
        if function_output == 'success':
            output_performative_type = 'inform_done'
            output_result = 'success'
            comments = None
        else:
            output_performative_type = 'failure'
            output_result = None
            comments = function_output
    elif performative_type == 'request_di_change':
        function_output = di_change(content)
        if function_output == 'success':
            output_performative_type = 'inform_done'
            output_result = 'success'
            comments = None
        else:
            output_performative_type = 'failure'
            output_result = None
            comments = function_output
    elif performative_type == 'accepted_job_proposal':
        function_output = job_assignment(content)
        if function_output == 'success':
            output_performative_type = 'inform_done'
            output_result = 'success'
            comments = None
        else:
            output_performative_type = 'failure'
            output_result = None
            comments = function_output
    else:
        output_performative_type = None
        output_result = None
        comments = None
    output_dict = {'performative_type': output_performative_type, 'result': output_result, 'comments': comments}
    return output_dict
