import importlib
import os
import json
from datetime import datetime
from BaseLibraries.messaging import  message_to_json
import random
import string


# =====================================================================================================
#                   CREATE A LOG FILE
# =====================================================================================================


def create_new_log(message, paths_dictionary):
    protocol = message.protocol
    active_conv_folder = paths_dictionary["active_conversations_path"]
    if protocol in ['fipa request', 'request interaction protocol',
                    'request protocol', 'fipa request protocol', 'request_interaction_protocol']:
        folder_location = active_conv_folder + r"\request_interaction_protocol"

    elif protocol in ['fipa request when', 'request_when_interaction_protocol',
                      'request when protocol', 'fipa request-when protocol', 'fipa request when protocol',
                      'request-when protocol']:
        folder_location = active_conv_folder + r"\request_when_interaction_protocol"

    elif protocol in ['fipa propose', 'propose_interaction_protocol',
                      'propose protocol', 'fipa propose protocol']:
        folder_location = active_conv_folder + r"\propose_interaction_protocol"

    elif protocol in ['fipa subscribe', 'subscribe_interaction_protocol',
                      'subscribe protocol', 'fipa subscribe protocol']:
        folder_location = active_conv_folder + r"\subscribe_interaction_protocol"

    elif protocol in ['fipa contract-net', 'contract-net interaction protocol',
                      'contract_net_protocol', 'contract net protocol',
                      'contract_net_interaction_protocol',
                      'fipa contract net protocol',
                      'fipa contract-net protocol', 'contract-net protocol']:
        folder_location = active_conv_folder + r"\contract_net_interaction_protocol"

    elif protocol in ['fipa query interaction protocol', 'query_interaction_protocol',
                      'query protocol', 'fipa query protocol']:
        folder_location = active_conv_folder + r"\query_interaction_protocol"

    elif protocol in ['fipa broking interaction protocol', 'broking_interaction_protocol',
                      'broking protocol', 'fipa broking protocol']:
        folder_location = active_conv_folder + r"\broking_interaction_protocol"

    elif protocol in ['fipa recruiting interaction protocol', 'recruiting_interaction_protocol',
                      'recruiting protocol', 'fipa recruiting protocol']:
        folder_location = active_conv_folder + r"\recruiting_interaction_protocol"

    log_file_name = fr"\{message.conversation_id}" + ".json"
    print("inside create new log")
    data = {}
    timestamp = str(datetime.now())
    data[message.performative] = [[timestamp, message_to_json(message)]]
    with open((folder_location + fr"\{log_file_name}"), "w+") as outfile:
        json.dump(data, outfile)

    outfile.close()
    return

# =====================================================================================================
#                   LOG AND CONTINUE FUNCTION
# =====================================================================================================


def log_and_continue(message, paths_dictionary):
    protocol = message.protocol

    active_conv_folder = paths_dictionary["active_conversations_path"]
    if protocol in ['fipa request', 'request interaction protocol',
                    'request protocol', 'fipa request protocol', 'request_interaction_protocol']:
        folder_location = active_conv_folder + r"\request_interaction_protocol"

    elif protocol in ['fipa request when', 'request when interaction protocol',
                      'request when protocol', 'fipa request-when protocol', 'fipa request when protocol',
                      'request-when protocol']:
        folder_location = active_conv_folder + r"\request_when_interaction_protocol"

    elif protocol in ['fipa propose', 'propose interaction protocol',
                      'propose protocol', 'fipa propose protocol']:
        folder_location = active_conv_folder + r"\propose_interaction_protocol"

    elif protocol in ['fipa subscribe', 'subscribe interaction protocol',
                      'subscribe protocol', 'fipa subscribe protocol']:
        folder_location = active_conv_folder + r"\subscribe_interaction_protocol"

    elif protocol in ['fipa contract-net', 'contract-net interaction protocol',
                      'contract_net_protocol', 'contract net protocol',
                      'contract net interaction protocol',
                      'fipa contract net protocol',
                      'fipa contract-net protocol', 'contract-net protocol']:
        folder_location = active_conv_folder + r"\contract_net_interaction_protocol"

    elif protocol in ['fipa query interaction protocol', 'query interaction protocol',
                      'query protocol', 'fipa query protocol']:
        folder_location = active_conv_folder + r"\query_interaction_protocol"

    elif protocol in ['fipa broking interaction protocol', 'broking interaction protocol',
                      'broking protocol', 'fipa broking protocol']:
        folder_location = active_conv_folder + r"\broking_interaction_protocol"

    elif protocol in ['fipa recruiting interaction protocol', 'recruiting interaction protocol',
                      'recruiting protocol', 'fipa recruiting protocol']:
        folder_location = active_conv_folder + r"\recruiting_interaction_protocol"

    log_file_name = message.conversation_id + ".json"
    print("inside log and continue")
    with open((folder_location + fr"\{log_file_name}"), "r") as json_file:
        data = json.load(json_file)

    timestamp = str(datetime.now())
    try:
        data[message.performative].append([timestamp, message_to_json(message)])
    except:
        data[message.performative] = [timestamp, message_to_json(message)]

    with open((folder_location + fr"\{log_file_name}"), "w") as json_file:
        json.dump(data, json_file)
        json_file.close()
    return




# ----------------------------------------------------------------------------------------------------------------------


def log_and_end(message,paths_and_log_count):
    active_conv_folder = paths_and_log_count["active_conversations_path"]

    protocol = message.protocol
    active_conv_folder = paths_and_log_count["active_conversations_path"]
    if protocol in ['fipa request', 'request interaction protocol',
                    'request protocol', 'fipa request protocol', 'request_interaction_protocol']:
        folder_location = active_conv_folder + r"\request_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"


    elif protocol in ['fipa request when', 'request when interaction protocol',
                      'request when protocol', 'fipa request-when protocol', 'fipa request when protocol',
                      'request-when protocol']:
        folder_location = active_conv_folder + r"\request_when_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa propose', 'propose interaction protocol',
                      'propose protocol', 'fipa propose protocol']:
        folder_location = active_conv_folder + r"\propose_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa subscribe', 'subscribe interaction protocol',
                      'subscribe protocol', 'fipa subscribe protocol']:
        folder_location = active_conv_folder + r"\subscribe_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa contract-net', 'contract-net interaction protocol',
                      'contract_net_protocol', 'contract net protocol',
                      'contract net interaction protocol',
                      'fipa contract net protocol',
                      'fipa contract-net protocol', 'contract-net protocol']:
        folder_location = active_conv_folder + r"\contract_net_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa query interaction protocol', 'query interaction protocol',
                      'query protocol', 'fipa query protocol']:
        folder_location = active_conv_folder + r"\query_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa broking interaction protocol', 'broking interaction protocol',
                      'broking protocol', 'fipa broking protocol']:
        folder_location = active_conv_folder + r"\broking_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    elif protocol in ['fipa recruiting interaction protocol', 'recruiting interaction protocol',
                      'recruiting protocol', 'fipa recruiting protocol']:
        folder_location = active_conv_folder + r"\recruiting_interaction_protocol"
        filenames = os.listdir(folder_location)  # filenames in folder of active and passive functions
        for filename in filenames:
            if filename[:-4] == message.conversation_id:
                log_file_name = message.conversation_id + ".json"

    log_file_name = message.conversation_id + ".json"
    print("inside log and end")
    with open((folder_location + fr"\{log_file_name}"), "r") as json_file:
        data = json.load(json_file)

    timestamp = str(datetime.now())
    try:
        data[message.performative].append([timestamp, message_to_json(message)])
    except:
        data[message.performative] = [timestamp, message_to_json(message)]

    with open((folder_location + fr"\{log_file_name}"), "w") as json_file:
        json.dump(data, json_file)
        json_file.close()

    return


