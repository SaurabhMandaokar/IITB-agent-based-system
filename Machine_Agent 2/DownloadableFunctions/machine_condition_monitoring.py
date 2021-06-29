#ACTIVE

import pickle

def introduction():
    function_type = 'Machine Condition Monitoring'
    dependant_functions = []
    active_passive = 'Active'
    return {'Function Type':function_type,'Dependant Function':dependant_functions, 'active_passive' : active_passive}


def callable():
    with open("DataBase\\machine_condition_monitoring\\maintenance_schedule.txt", "rb") as maintenance_schedule_data:
        maintenance_schedule = pickle.load(maintenance_schedule_data)
    return maintenance_schedule
    

def Active():
    print('CBM Start')
    import numpy as np
    import pandas as pd
    import math
    import pickle
    from pickle import dump, load
    from datetime import timedelta
    from datetime import date
    import time
##    from keras.models import Sequential
##    from keras.layers import Dense
##    from keras.layers import LSTM
##    from keras.models import load_model
##    from sklearn.metrics import mean_squared_error
##    import tensorflow as tf
##    from tensorflow.keras.preprocessing.sequence import pad_sequences
##    from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional, Conv1D, MaxPooling1D
##    from tensorflow.keras.preprocessing.text import Tokenizer
##    from tensorflow.keras.models import Sequential
##    from tensorflow.keras.optimizers import Adam

##    min_max_scaler = load(open('DataBase\\machine_condition_monitoring\\min_max_scaler.pkl', 'rb'))
##    model = load_model('DataBase\\machine_condition_monitoring\\model.h5', 'rb')


    with open("DataBase\\machine_condition_monitoring\\q_table_data.txt", "rb") as q_table_data:
        q_table_data = pickle.load(q_table_data)


    data_pointing_table={}
    data_pointing_table_file = open("MachineCommunicationConfig.txt")
    data_pointing_table_file_contents = data_pointing_table_file.read()
    Lines = data_pointing_table_file_contents.splitlines()
    for line in Lines:
        key,value=line.split("=>")
        data_pointing_table[key] = value
    data_file_name='MachineCommunication\\'+data_pointing_table['machine_condition_monitoring']

    while True:
        #importing data from csv 
        sensor_data = np.array([[np.genfromtxt(data_file_name, delimiter=',')]])
##        print(sensor_data)
##        predicted_rul = min_max_scaler.inverse_transform(model.predict(sensor_data))
##        predicted_rul = predicted_rul.reshape(-1)
##        #print('Predicted RUL result from Loaded Model ->',predicted_rul)

        
        predicted_rul=[22]
        maintenance_action,interval=q_table_data[predicted_rul[0]]

        output={}
        if maintenance_action=='NA':
            output['maintenance action']='NA'
            output['maintenance date']='NA'
            output['maintenance time']='NA'
        elif maintenance_action=='MM':
            next_maintenance_date = (date.today()+timedelta(days=interval)).strftime("%m-%d-%Y")
            output['maintenance action']='MM'
            output['maintenance date']=next_maintenance_date
            output['maintenance time in day']=1
        elif maintenance_action=='PM':
            next_maintenance_date = (date.today()+timedelta(days=interval)).strftime("%m-%d-%Y")
            output['maintenance action']='PM'
            output['maintenance date']=next_maintenance_date
            output['maintenance time']=2

        print(output)
        a_file = open("DataBase\\machine_condition_monitoring\\maintenance_schedule.txt", "wb")
        pickle.dump(output, a_file)
        a_file.close()

        time.sleep(60*60*24*interval)
    
