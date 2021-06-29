import csv
import socket
import threading
from BaseLibraries.messaging import *
from tkinter import *
from datetime import datetime
import time
from BaseLibraries.support_files import *
from BaseLibraries.handlers import message_handler
from tkinter import Tk, Button, Label, ttk
from tkinter.scrolledtext import ScrolledText
from BaseLibraries.conversation_logging import create_new_log
from BaseLibraries.advanced_messaging import check_advanced_communications
import pandas as pd
import queue

# ===========================================================================================
#                           BEFORE CONTACTING SERVER
# =========================================================================================


# to create type to function mapping and function pointing files

msg_to_send_queue = queue.Queue()
timed_reply_queue = queue.Queue()
allotment_queue = queue.Queue()

global nickname
# nickname = input("Choose a nickname: ")
nickname = 'Job_Manager'
nicknames = []
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 6525))

agent_role = 'job_manager'
parent_folder_path = r'C:\Users\Saourabh\PycharmProjects\Jobs_Manager'
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

# ----------------------------------------------------------------------------------------- #
#                 GUI and "functions to put something on GUI" start from here               #
# ----------------------------------------------------------------------------------------- #
root = Tk()
root.title(f'{nickname}: manual FIPA messaging')
root.geometry("1200x700")

global tree_count
tree_count = 0

text_area = ScrolledText(root, width=40, height=40)
text_area.grid(row=1, column=4, padx=20, pady=5, columnspan=2, rowspan=15)
text_area.config(state='disabled')


# def gui_entries_to_msg(entry_list):
#     # 0. receiver 1. protocol 2.performative 3. type 4. content
#     message = FIPA_message()
#     message.sender = nickname
#     message.receiver = str([listbox_receivers.get(item) for item in listbox_receivers.curselection()])
#     message.protocol = entry_list[1].get()
#     message.performative = entry_list[2].get()
#     message.type = entry_list[3].get()
#     message.content = entry_list[4].get()
#
#     return message


def targets_identifier(performative_type):
    agent_directory_folder_path = paths_dictionary['agents_directory']
    filenames = os.listdir(agent_directory_folder_path)  # filenames in folder of active and passive functions
    receivers_list = []
    for filename in filenames:
        if filename[-5:] == '.json':
            print(filename)
            with open(agent_directory_folder_path + f"\{filename}", 'r') as j:
                json_file = json.load(j)
            if json_file[performative_type]['receive'] in [1, '1']:
                receivers_list.append(filename[:-5])
            j.close()

    return receivers_list


def log_allotment(Ji, Pi, Di, Ei, Li):
    alloted_agent = allotment_queue.get()
    with open(paths_dictionary['database'] + r"\SingleMechineSequencing\job_data_Li_Ei.csv", "a") as csv_file:
        csv_file.write(f"{Ji},{Pi},{Di},{Ei},{Li},{alloted_agent}\n")

    csv_file.close()

    global tree_count
    my_tree.insert(parent='', index='end', iid=tree_count, text=tree_count,
                   values=(Ji, Pi, Di, Ei, Li, alloted_agent))
    tree_count += 1
    return


def new_job_arrival():
    # 0. receiver 1. protocol 2.performative 3. type 4. content
    Ji, Pi, Di, Ei, Li = all_entries[0].get(), all_entries[1].get(), all_entries[2].get(), all_entries[3].get(), all_entries[4].get()
    print("Ji, Pi, Di, Ei, Li :",Ji, Pi, Di, Ei, Li)
    message = FIPA_message()
    message.sender = nickname
    message.protocol = 'contract_net_interaction_protocol'
    message.performative = "call_for_proposal"
    message.type = "cfp_for_new_job_arrival"
    message.receiver = str(targets_identifier(message.type))
    message.content = [int(Ji), int(Pi), Di, int(Ei), int(Li)]

    # print("printing from new job arrival fn:", message.content)
    message.conversation_id = set_conversation_id(message)
    msg_to_send_queue.put(message)
    entry_Ji.delete(0, END)
    entry_Pi.delete(0, END)
    entry_Di.delete(0, END)
    entry_Ei.delete(0, END)
    entry_Li.delete(0, END)

    allotment_thread = threading.Thread(target = log_allotment, args=[Ji, Pi, Di, Ei, Li,])
    allotment_thread.start()

    return


def update_job_Details():
    Ji, Pi, Di, Ei, Li = all_entries[0].get(), all_entries[1].get(), all_entries[2].get(), all_entries[3].get(), \
                         all_entries[4].get()
    new_rows = []
    with open(paths_dictionary['database'] + r"\SingleMechineSequencing\job_data_Li_Ei.csv", "r") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=',')
        for line in file_reader:
            if line[0] == Ji:
                line[1] = Pi
                line[2] = Di
                line[3] = Ei
                line[4] = Li
                target_agent = line[5]
            new_rows.append(line)

    with open(paths_dictionary['database'] + r"\SingleMechineSequencing\job_data_Li_Ei.csv", "w") as csv_file:
        for row in new_rows:
            csv_file.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n")

    selected_job = my_tree.focus()
    my_tree.item(selected_job,text='',values=(Ji, Pi, Di, Ei, Li,target_agent))
    message = FIPA_message()
    message.sender = nickname
    message.protocol = 'request_interaction_protocol'
    message.performative = "request"
    message.type = "request_di_change"
    message.receiver = target_agent
    message.content = [int(Ji), int(Pi), Di, int(Ei), int(Li)]
    print("printing from new job arrival fn:", message.content)
    message.conversation_id = set_conversation_id(message)
    msg_to_send_queue.put(message)

    entry_Ji.delete(0, END)
    entry_Pi.delete(0, END)
    entry_Di.delete(0, END)
    entry_Ei.delete(0, END)
    entry_Li.delete(0, END)

    return


def load_selected_job():
    entry_Ji.delete(0, END)
    entry_Pi.delete(0, END)
    entry_Di.delete(0, END)
    entry_Ei.delete(0, END)
    entry_Li.delete(0, END)

    selected_row = my_tree.focus()
    values = my_tree.item(selected_row, 'values')

    entry_Ji.insert(0, values[0])
    entry_Pi.insert(0, values[1])
    entry_Di.insert(0, values[2])
    entry_Ei.insert(0, values[3])
    entry_Li.insert(0, values[4])
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
        time.sleep(0.1)
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
            advanced_comm_thread = threading.Thread(target=check_advanced_communications,
                                                    args=[message, timed_reply_queue, msg_to_send_queue,
                                                          paths_dictionary, ])
            advanced_comm_thread.start()


all_entries = []
# all labels
message_parameters = ["Job Id", "processing Time", "Due Date", "Early Penalty", "Late Penalty"]
for i in range(0, len(message_parameters)):
    label2 = Label(root, text=message_parameters[i])
    label2.grid(row=i + 1, column=0)

# Job-id entry
entry_Ji = Entry(root, width=30)
entry_Ji.grid(row=1, column=1, pady=5)
entry_Ji.insert(0,2)
all_entries.append(entry_Ji)

# processing_time entry
entry_Pi = Entry(root, width=30)
entry_Pi.grid(row=2, column=1)
entry_Pi.insert(0,23)
all_entries.append(entry_Pi)

# Due Date entry
entry_Di = Entry(root, width=30)
entry_Di.grid(row=3, column=1)
entry_Di.insert(0,'06-15-2021')
all_entries.append(entry_Di)

# Early Penalty
entry_Ei = Entry(root, width=30)
entry_Ei.grid(row=4, column=1)
entry_Ei.insert(0,21)
all_entries.append(entry_Ei)

# Late Penalty
entry_Li = Entry(root, width=30)
entry_Li.grid(row=5, column=1)
entry_Li.insert(0,32)
all_entries.append(entry_Li)

# receivers entry by listbox multiselect mode
listbox_receivers = Listbox(root, width=30, height=10, selectmode=MULTIPLE)
listbox_receivers.grid(row=7, column=1)
clicked_agents = listbox_receivers.curselection()
all_entries.append(clicked_agents)

my_tree = ttk.Treeview(root)
df = pd.read_csv(r"C:\Users\Saourabh\PycharmProjects\Jobs_Manager\DataBase\SingleMechineSequencing\job_data_Li_Ei.csv")
my_tree['columns'] = ('Ji', 'pi', 'di', 'ei', 'Li', 'allotment')
my_tree.column("#0", width=120, minwidth=25)
my_tree.column("Ji", anchor=W, width=120)
my_tree.column("pi", anchor=W, width=110)
my_tree.column("di", anchor=CENTER, width=80)
my_tree.column("ei", anchor=W, width=100)
my_tree.column("Li", anchor=W, width=90)
my_tree.column("allotment", anchor=W, width=90)

my_tree.heading("#0", text='sr. no', anchor=W)
my_tree.heading("Ji", text="Ji")
my_tree.heading("pi", text="pi")
my_tree.heading("di", text="di")
my_tree.heading("ei", text="ei")
my_tree.heading("Li", text="Li")
my_tree.heading("allotment", text="allotment")

with open(paths_dictionary['database'] + r"\SingleMechineSequencing\job_data_Li_Ei.csv", "r") as csv_file:
    file_reader = csv.reader(csv_file, delimiter=',')
    head = next(file_reader)
    for line in file_reader:

        my_tree.insert(parent='', index='end', iid=tree_count, text=tree_count,
                       values=(line[0], line[1], line[2], line[3], line[4], line[5]))

        tree_count += 1
my_tree.grid(row=8, column=0, columnspan=3)

button1 = Button(root, text="add new job", command=new_job_arrival)
button1.grid(row=6, column=0, padx=5)

button2 = Button(root, text="Di change", command=update_job_Details)
button2.grid(row=6, column=1)

button3 = Button(root, text="Pi change", command=update_job_Details)
button3.grid(row=6, column=2)

button4 = Button(root, text="load selected job", command=load_selected_job)
button4.grid(row=5, column=2)

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

    handle_and_send_thread = threading.Thread(target=message_handler,
                                              args=[message, msg_to_send_queue, paths_dictionary,allotment_queue, ])
    handle_and_send_thread.start()


def receive():
    while True:
        # try:
        message = client.recv(1024)
        if len(message) > 0:
            msg = message
            while len(message) > 1023:
                message = client.recv(1024)
                msg += message

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


queues_thread = threading.Thread(target=print_on_GUI_and_send_from_queue, args=[msg_to_send_queue, ])
receive_thread = threading.Thread(target=receive)

queues_thread.start()
receive_thread.start()

root.mainloop()
