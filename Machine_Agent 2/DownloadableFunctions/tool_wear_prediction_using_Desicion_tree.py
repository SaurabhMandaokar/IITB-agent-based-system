#ACTIVE

def introduction():
    function_type = 'Tool Condition Monitoring'
    dependant_functions = ['Single Machine Sequencing with Maintenance Consideration']
    active_passive = 'Active'
    performative_types = ['cfp_for_job_of_failed_machine']
    return {'Function Type':function_type,'Dependant Function':dependant_functions, 'active_passive' : active_passive}


def callable():
    data_pointing_table_file = open("DataBase\\tool_wear_prediction_using_Desicion_tree\\tool_wear_class.txt")
    data_pointing_table_file_contents = data_pointing_table_file.read()
    return data_pointing_table_file_contents
    

def Active():
    import numpy as np
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    import pickle
    import time
    import threading
    import DownloadableFunctions


    function_pointing_table={}
    function_pointing_table_file = open("FunctionPointingConfig.txt")
    function_pointing_table_file_contents = function_pointing_table_file.read()
    Lines = function_pointing_table_file_contents.splitlines()
    for line in Lines:
        key_values=line.split("=>")
        key=key_values[0]
        value=(key_values[1]).split("|")
        function_pointing_table[key] = value


    dependancy_list=function_pointing_table['tool_wear_prediction_using_Desicion_tree']
    for element in dependancy_list:
        key,value=element.split("->")
        if key == 'Single Machine Sequencing with Maintenance Consideration':
            module_name=value
            break

    filename = 'DataBase\\tool_wear_prediction_using_Desicion_tree\\tool_wear_classification_decision_tree_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))


    data_pointing_table={}
    data_pointing_table_file = open("MachineCommunicationConfig.txt")
    data_pointing_table_file_contents = data_pointing_table_file.read()
    Lines = data_pointing_table_file_contents.splitlines()
    for line in Lines:
        key,value=line.split("=>")
        data_pointing_table[key] = value

    data_file_name='MachineCommunication\\'+data_pointing_table['tool_wear_prediction_using_Desicion_tree']

    time_for_maintenace = 2
    
    while True:
        #importing data from csv 
        data = pd.read_csv(data_file_name)
        #print ('###### data ######')
        #print (data)
        predicted_result=loaded_model.predict(data)
        #print('predicted result from Loaded Model ->',predicted_result)
        #print ('################################################')
        predicted_result=predicted_result[0]
        if predicted_result[0]==1:
            tool_wear_class=1
        elif predicted_result[1]==1:
            tool_wear_class=2
        elif predicted_result[2]==1:
            tool_wear_class=3
        elif predicted_result[3]==1:
            tool_wear_class=4
            
            string='machine_fail_thread=threading.Thread(target=DownloadableFunctions.'+module_name+'.machine_fail,args=[time_for_maintenace]).start()'
            exec(string)
            
        f = open("DataBase\\tool_wear_prediction_using_Desicion_tree\\tool_wear_class.txt", "w")
        f.write(str(tool_wear_class))
        f.close()
        time.sleep(60)
    
