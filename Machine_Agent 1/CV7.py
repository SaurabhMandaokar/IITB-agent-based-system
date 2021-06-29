import csv
import queue
import socket
# -----------------------------------------------------
import threading
from tkinter import *
from tkinter import Tk, Button, Label, ttk
from tkinter.scrolledtext import ScrolledText

from BaseLibraries.advanced_messaging import check_advanced_communications
from BaseLibraries.conversation_logging import create_new_log
from BaseLibraries.handlers import message_handler
from BaseLibraries.messaging import *
from BaseLibraries.support_files import *

# -----------------------------------------------------------------------------
from DownloadableFunctions import Single_Machine_Sequencing_Considering_Maintenace_Action

function_pointing_table={}
function_pointing_table_file = open("FunctionPointingConfig.txt")
function_pointing_table_file_contents = function_pointing_table_file.read()
Lines = function_pointing_table_file_contents.splitlines()
for line in Lines:
    key_values=line.split("=>")
    key=key_values[0]
    value=(key_values[1]).split("|")
    function_pointing_table[key] = value
print(function_pointing_table)


function_available_table={}
function_available_table_file = open("AvailableFunctions.txt")
function_available_table_file_contents = function_available_table_file.read()
Lines = function_available_table_file_contents.splitlines()
for line in Lines:
    key_values=line.split("=>")
    key=key_values[0]
    value=(key_values[1]).split("|")
    function_available_table[key] = value
##print(function_available_table)

ActiveFunctionsList = open("ActiveFunctionsList.txt")
ActiveFunctionsList_contents = ActiveFunctionsList.read()
Lines = ActiveFunctionsList_contents.splitlines()
for line in Lines:
    key,value=line.split("=>")
    if value=='1':
        print(key)
        string=key+"_thread=threading.Thread(target="+key+".Active).start()"
        print(string)
        exec(string)


# -----------------------------------------------------


# ===========================================================================================
#                           BEFORE CONTACTING SERVER
# =========================================================================================


# to create type to function mapping and function pointing files

msg_to_send_queue = queue.Queue()
timed_reply_queue = queue.Queue()



protocols_list = ['contract_net_interaction_protocol', 'request_interaction_protocol', 'request-when_interaction_protocol',
                  'query_interaction_protocol', 'broking_interaction_protocol',
                  'recruiting_interaction_protocol',
                  'propose interaction protocol', 'subscribe interaction protocol']

performatives_list = ['call_for_proposal','request', 'accept_proposal', 'agree', 'cancel',  'confirm',
                      'disconfirm', ' failure', 'inform', 'inform_if', 'inform-ref'
    , 'not_understood', 'propagate', 'propose', 'proxy', 'query_if',
                      'query_ref', 'refuse', 'reject_proposal', 'request_when'
                                                                'request_whenever', 'subscribe']

global nickname
# nickname = input("Choose a nickname: ")
nickname = 'machine-Agent 1'
nicknames = []

agent_role = 'machine_agent'
parent_folder_path = r'C:\Users\Saourabh\PycharmProjects\Machine_Agent 1'
paths_dictionary = {}
paths_dictionary['agent_functions_path'] = parent_folder_path + r'\DownloadableFunctions'
paths_dictionary[
    'active_conversations_path'] = parent_folder_path + r"\Conversation_Logs\active_conversations"
paths_dictionary[
    'ended_coversations_path'] = parent_folder_path + r"\Conversation_Logs\ended_conversations"
paths_dictionary[
    'active_functions_configuration'] = parent_folder_path + r"\active_functions_config.txt"
paths_dictionary['agents_directory'] = parent_folder_path + r"\agents_directory"
paths_dictionary['database'] = parent_folder_path + r"\DataBase"
paths_dictionary['agent_name'] = nickname
paths_dictionary['agent_role'] = agent_role

create_mapping_and_pointing_files(paths_dictionary, msg_to_send_queue)



global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 6525))


# ----------------------------------------------------------------------------------------- #
#                 GUI and "functions to put something on GUI" start from here               #
# ----------------------------------------------------------------------------------------- #
root = Tk()
root.title(f'{nickname}: manual FIPA messaging')
root.geometry("600x800")

text_area = ScrolledText(root, width=40, height=40)
text_area.grid(row=7, column=0, padx=20, pady=5, columnspan=2)
text_area.config(state='disabled')


def auction_all_jobs():
    jobs_list = []
    with open(paths_dictionary['database'] + r"\SingleMechineSequencing\job_data_Li_Ei.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # to ignore header
        for line in reader:
            jobs_list.append(line)
    print(jobs_list)

    for job in jobs_list:
        message = FIPA_message()
        message.protocol = 'contract_net_interaction_protocol'
        message.performative = 'call_for_proposal'
        message.type = 'cfp_for_job_of_failed_machine'
        message.sender = nickname
        message.receiver = str(targets_identifier(message.type))
        message.content = [int(job[0]), int(job[1]), job[2], int(job[3]), int(job[4])]
        message.conversation_id = set_conversation_id(message)
        msg_to_send_queue.put(message)

    return

def targets_identifier(performative_type):
    agent_directory_folder_path = paths_dictionary['agents_directory']
    filenames = os.listdir(agent_directory_folder_path)  # filenames in folder of active and passive functions
    receivers_list = []
    for filename in filenames:
        if filename[-5:] == '.json':
            print(filename)
            with open(agent_directory_folder_path + fr"\{filename}", 'r') as j:
                json_file = json.load(j)
            if json_file[performative_type]['receive'] in [1, '1']:
                receivers_list.append(filename[:-5])
            j.close()

    return receivers_list


def gui_entries_to_msg(entry_list):
    # 0. receiver 1. protocol 2.performative 3. type 4. content
    message = FIPA_message()
    message.sender = nickname
    message.receiver = str([listbox_receivers.get(item) for item in listbox_receivers.curselection()])
    message.protocol = entry_list[1].get()
    message.performative = entry_list[2].get()
    message.type = entry_list[3].get()
    message.content = entry_list[4].get()

    return message


# gui_sender is used while sending manual message through GUI button press
def gui_sender():
    text_area.config(state='normal')
    text_area.insert('end',
                     f" \n{nickname} ---> {str([listbox_receivers.get(item) for item in listbox_receivers.curselection()])} ")
    text_area.insert('end', f" \nprotocol: {all_entries[1].get()} ")
    text_area.insert('end', f" \nperformative: {all_entries[2].get()} ")
    text_area.insert('end', f" \ntype: {all_entries[3].get()} ")
    text_area.insert('end', f" \nContent: {all_entries[4].get()} ")
    text_area.insert('end', " \n -------------------- \n ")
    text_area.yview('end')
    text_area.config(state='disabled')

    msg = gui_entries_to_msg(all_entries)
    msg.conversation_id = set_conversation_id(msg)
    print(msg.conversation_id)
    msg_to_send_queue.put(msg)
    create_new_log(msg, paths_dictionary)
    all_entries[0] = []

    return

# print_text_on_GUI used for non-FIPA type messages for single line print on GUI
# input: string
def print_text_on_GUI(txt):
    text_area.config(state='normal')
    text_area.insert('end', f" \n Server ---> all ")
    text_area.insert('end', f" \n{txt} ")
    text_area.insert('end', " \n -------------------- \n ")
    text_area.yview('end')
    text_area.config(state='disabled')
    return


def print_on_GUI_and_send_from_queue(msg_to_send_queue):
    # just to print the messages that get sent on the GUI
    # message sender name is put here before sending
    while True:
        message = msg_to_send_queue.get()
        print(message.conversation_id)
        message.sender = nickname
        text_area.config(state='normal')
        text_area.insert('end', f" \n{message.sender} ---> {message.receiver} @ {message.conversation_id}")
        text_area.insert('end', f" \nprotocol: {message.protocol} ")
        text_area.insert('end', f" \nperformative: {message.performative} ")
        text_area.insert('end', f" \ntype: {message.type} ")
        text_area.insert('end', f" \nContent: {message.content} ")
        text_area.insert('end', " \n -------------------- \n ")
        text_area.yview('end')
        text_area.config(state='disabled')
        print(message.protocol, message.performative, message.content)
        client.send(flatten(message))
        if message.protocol == 'contract_net_interaction_protocol' and message.performative == 'call_for_proposal':
            advanced_comm_thread = threading.Thread(target = check_advanced_communications,
                                                    args= [message, timed_reply_queue, msg_to_send_queue, paths_dictionary,])
            advanced_comm_thread.start()



all_entries = []
# all labels
message_parameters = ["receiver", "protocol", "performative", "type", "content"]
for i in range(0, len(message_parameters)):
    label2 = Label(root, text=message_parameters[i])
    label2.grid(row=i, column=0)

# receivers entry by listbox multiselect mode
listbox_receivers = Listbox(root, width=30, height=10, selectmode=MULTIPLE)
listbox_receivers.grid(row=0, column=1)
clicked_agents = listbox_receivers.curselection()
all_entries.append(clicked_agents)

# protocols entry box
myCombo_protocols = ttk.Combobox(root, value=protocols_list)
myCombo_protocols.current(0)
myCombo_protocols.bind("<<ComboboxSelected>>")
myCombo_protocols.grid(row=1, column=1)
all_entries.append(myCombo_protocols)

# performatives entry box
myCombo_perf = ttk.Combobox(root, value=performatives_list)
myCombo_perf.current(0)
myCombo_perf.bind("<<ComboboxSelected>>")
myCombo_perf.grid(row=2, column=1)
all_entries.append(myCombo_perf)

# type entry
entry_type = Entry(root, width=30)
entry_type.grid(row=3, column=1)
entry_type.insert(0,"cfp_for_transport")
all_entries.append(entry_type)

#  content entry
entry_content = Entry(root, width=30)
entry_content.grid(row=4, column=1)
entry_content.insert(0,"[1,10]")
all_entries.append(entry_content)

button1 = Button(root, text="SEND", command=gui_sender)
button1.grid(row=5, column=1)

button2 = Button(root, text="Machine failed", command=auction_all_jobs)
button2.grid(row=5, column=2)

# ----------------------------------------------------------------------------------------- #
#                 Main Agent message handlers and response generation functions             #
# ----------------------------------------------------------------------------------------- #


def parentMessageHandler(message):
    print(message.content)
    # printing on GUI
    text_area.config(state='normal')
    text_area.insert('end', f" \n{message.sender} ---> {message.receiver} @ {message.conversation_id}")
    text_area.insert('end', f" \nprotocol: {message.protocol} ")
    text_area.insert('end', f" \nperformative: {message.performative} ")
    text_area.insert('end', f" \ntype: {message.type} ")
    text_area.insert('end', f" \nContent: {message.content} ")
    text_area.insert('end', " \n -------------------- \n ")
    text_area.yview('end')
    text_area.config(state='disabled')

    handle_and_send_thread = threading.Thread(target=message_handler, args=[message, msg_to_send_queue, paths_dictionary, ])
    handle_and_send_thread.start()

def receive():
    while True:
        # try:
        message = client.recv(1024)
        if len(message) > 0:
            msg = message
            while len(message) >1023:
                message = client.recv(1024)
                msg+=message

            msg = unflatten(message)
            # if the server send a NICK then
            # we send the nickname back
            if msg.protocol == "DUMMY_FIPA":
                if msg.type == "server_topics" and msg.content == 'NICK':
                    client.send(flatten(dummyFIPA("server_topics", nickname)))
                elif msg.type == "client_connected":  # this message is only sent once by server at initiation
                    print_text_on_GUI(f"{msg.content} is now connected ")
                    nicknames.append(msg.content)
                    listbox_receivers.insert('end', msg.content)



                elif msg.type == "client_disconnected":
                    print_text_on_GUI(f"{msg.content} is now disconnected ")
                    nickname_index = nicknames.index(msg.content)
                    nicknames.remove(msg.content)
                    listbox_receivers.delete(nickname_index)

                elif msg.type == "active_agents":  # this message is only sent once by server at initiation
                    for agent_nickname in msg.content:
                        if agent_nickname != nickname:
                            listbox_receivers.insert('end', agent_nickname)

                else:
                    print_text_on_GUI(msg.content)

            else:

                print(f"{msg.performative} received ", "cid = ", msg.conversation_id)
                timed_reply_queue.put(msg)
                parentMessageHandler(msg)

        # except:
        #     print("an error occurred")
        #     client.close()
        #     break


# if message is getting printed twice, it is because
# sender is printing it, and same message is being received by receiver
# as stuff is broadcasted and that gets printed as well!!


queues_thread = threading.Thread(target= print_on_GUI_and_send_from_queue, args = [msg_to_send_queue,])
receive_thread = threading.Thread(target=receive)

queues_thread.start()
receive_thread.start()

root.mainloop()
