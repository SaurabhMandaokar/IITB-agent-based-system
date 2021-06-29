# PASSIVE

import pandas as pd
from itertools import permutations
import os


##os.chdir('..')

####################################################################################
def introduction():
    function_type = 'Single Machine Sequencing'
    dependant_functions = []
    active_passive = 'Passive'
    return {'Function Type': function_type, 'Dependant Function': dependant_functions, 'active_passive': active_passive}


####################################################################################
# Defined cost function
# Here linear cost function is defined
def cost_function(p, d, l, e):
    if p > d:
        return (p - d) * l
    else:
        return (d - p) * e


# ##################################################################################
def penalty_and_optimal_sequence(data):
    ####################################################################################
    # calculating total processing time
    total_p = sum(data['Pi'])
    # print('total processing time:',total_p)

    # all job index is saved in variable all_index
    all_index = list(data.index)

    # Creating a list named 'possible_seq' which contains all sequence condiates for the for the problem
    # we initialise list with cost = inf
    possible_seq = [[[], all_index, float('inf')]]
    # print('Init Seq: ',possible_seq)

    ####################################################################################
    # Run while loop till we get optimised solution
    while True:

        # find node of tree with min cost
        node = min(possible_seq, key=lambda x: x[2])
        ##print(node)

        # if selected node is leaf or no subtree can be formed from node we break the loop
        if (node[1] == []):
            break

        # number of braches can be formed out of node is depend on node[1]
        # we form number of braches depending upon elements in node[1]
        for i in node[1]:
            # form new brach with posiible seq
            element1 = node[0] + [i]
            element2 = list(set(node[1]) - set([i]))

            # calculating cost of the branch
            p = 0
            for j in element2:
                p += data['Pi'][j]

            r_element1 = element1.copy()
            r_element1.reverse()
            cost = 0
            for j in r_element1:
                p += data['Pi'][j]
                cost += cost_function(p, data['Di'][j], data['Li'][j], data['Ei'][j])

            # appending brach (sequence) in the 'possible_seq' list
            # print(element1,element2,cost)
            possible_seq.append([element1, element2, cost])

        # removing node from 'possible_seq'
        possible_seq.remove(node)
        ##print(possible_seq)

    ####################################################################################
    # Sequence with least cost is found using following line
    # Sequence is in reversed order
    node = min(possible_seq, key=lambda x: x[2])
    ##print(node)

    # node[0] is the solution, it is the reversed order of optimal solution
    # print()
    # print('Job Seq: ',end=' ')
    req_seq = (node[0])
    # we reverse the list to get actual optimal solution
    req_seq.reverse()
    # print the optimal sequence
    optimal_seq = []
    for i in req_seq:
        # print(data['Ji'][i],end=' ')
        optimal_seq.append(data['Ji'][i])
    # print()
    # print('Penalty = ',node[2])

    return {'penalty': node[2], 'optimal queue': optimal_seq}

    ####################################################################################


####################################################################################
def current_queue():
    return pd.read_csv('DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv')


####################################################################################
def update_current_queue(data):
    data.to_csv("DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv", index=False)
    return 'success'


####################################################################################
def update_optimal_queue(optimal_queue):
    Output_file = open("DataBase\\SingleMechineSequencing\\current_optimal_queue.csv", "w")
    for i in range(len(optimal_queue) - 1):
        Output_file.write(str(optimal_queue[i]))
        Output_file.write(",")
    if len(optimal_queue) > 0:
        Output_file.write(str(optimal_queue[-1]))
    Output_file.close()
    return 'success'


####################################################################################
def new_job_arrival_penalty(new_job_data):
    data = pd.read_csv('DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv')
    row_number = len(data)
    data.loc[row_number] = new_job_data
    # print(data)
    data['Di'] = pd.to_datetime(data['Di'])
    data['Di'] = (data['Di'] - pd.Timestamp.now().normalize()).dt.days
    # print(data)
    penalty_optimal_seq_data = penalty_and_optimal_sequence(data)
    return (penalty_optimal_seq_data['penalty'])


####################################################################################
def pi_change(job_data):
    data = pd.read_csv('DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv')
    # print(data)
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        return 'Job is not in the queue'
    else:
        data.loc[row_location[0]] = job_data
        data.to_csv("DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv", index=False)
        penalty_optimal_seq_data = penalty_and_optimal_sequence(data)
        optimal_queue = penalty_optimal_seq_data['optimal queue']
        # print(optimal_queue)
        if 'success' == update_optimal_queue(optimal_queue):
            return 'success'
        else:
            return 'error'


####################################################################################
def di_change(job_data):
    data = pd.read_csv('DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv')
    # print(data)
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        return 'Job is not in the queue'
    else:
        data.loc[row_location[0]] = job_data
        data.to_csv("DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv", index=False)
        penalty_optimal_seq_data = penalty_and_optimal_sequence(data)
        optimal_queue = penalty_optimal_seq_data['optimal queue']
        # print(optimal_queue)
        if 'success' == update_optimal_queue(optimal_queue):
            return 'success'
        else:
            return 'error'


####################################################################################
def job_assignment(job_data):
    data = pd.read_csv('DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv')
    row_location = data[data['Ji'] == job_data[0]].index.values
    if len(row_location) == 0:
        row_number = len(data)
        data.loc[row_number] = job_data
        data.to_csv("DataBase\\SingleMechineSequencing\\job_data_Li_Ei.csv", index=False)
        # print(data)
        data['Di'] = pd.to_datetime(data['Di'])
        data['Di'] = (data['Di'] - pd.Timestamp.now().normalize()).dt.days
        # print(data)
        penalty_optimal_seq_data = penalty_and_optimal_sequence(data)
        optimal_queue = penalty_optimal_seq_data['optimal queue']
        # print(optimal_queue)
        if 'success' == update_optimal_queue(optimal_queue):
            return 'success'
        else:
            return 'error'
    else:
        return 'Job is already in the queue'

####################################################################################


##print(new_job_arrival_penalty([20,20,'2021-06-06',4,5]))
##print(pi_change([13,20,'2021-06-07',4,5]))
##print(job_assignment([20,20,'2021-06-06',4,4]))
