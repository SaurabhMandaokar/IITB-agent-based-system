import json
import pickle
import random
import string


def flatten(message):
    # input is message object
    # output is serialized pickle message
    if message.content:
        msg = message_to_json(message)
        msg = json.dumps(msg)
        msg = pickle.dumps(msg)
        return msg


def unflatten(pickle_message):
    # unflatten requires a pickle message
    # output is message object
    msg = json.loads(pickle.loads(pickle_message))
    message = json_to_message(msg)
    return message


def dummyFIPA(non_FIPA_message_type, someString):
    # the input must be a string and
    # o/p is a fipa message object
    m = FIPA_message()
    m.protocol = "DUMMY_FIPA"
    m.content = someString
    m.type = non_FIPA_message_type
    return m


class FIPA_message:
    def __init__(self):
        self.protocol = None
        self.performative = None
        self.sender = None
        self.receiver = None
        self.content = None
        self.ontology = None
        self.format = None
        self.reply_to = None
        self.reply_by = None
        self.conversation_id = None
        self.type = None
        self.reply_to_type = None


# ---------------------------------------*
# #to convert message object into JSON   |
# -----------------------------------------
def message_to_json(message):
    msg = {}
    if message.protocol:
        msg['protocol'] = message.protocol
    if message.content:
        msg['content'] = message.content
    if message.ontology:
        msg['ontology'] = message.ontology
    if message.format:
        msg['format'] = message.format
    if message.sender:
        msg['sender'] = message.sender
    if message.receiver:
        msg['receiver'] = message.receiver
    if message.performative:
        msg['performative'] = message.performative
    if message.type:
        msg['type'] = message.type
    if message.reply_to_type:
        msg['type'] = message.reply_to_type
    if message.conversation_id:
        msg['conversation_id'] = message.conversation_id

    return msg


# -----------------------------------------------*
# #to convert JSON message into message object   |
# -----------------------------------------------*

def json_to_message(file):  # file--> JSON file on primary memory(RAM)...{'like': 'this'}. and not the path ...
    message = FIPA_message()
    for parameter in file:  # or you can also do parameter.lower()
        parameter = parameter.lower()
        if parameter == 'protocol':
            message.protocol = file[parameter]
        if parameter == 'content':
            message.content = file[parameter]
        if parameter == 'performative':
            message.performative = file[parameter]
        if parameter == 'conversation_id':
            message.conversation_id = file[parameter]
        if parameter == 'ontology':
            message.ontology = file[parameter]
        if parameter == 'format':
            message.format = file[parameter]
        if parameter == 'sender':
            message.sender = file[parameter]
        if parameter == 'receiver':
            message.receiver = file[parameter]
        if parameter == 'reply_to':
            message.reply_to = file[parameter]
        if parameter == 'reply_by':
            message.reply_by = file[parameter]
        if parameter == 'reply_to_type':
            message.reply_to_type = file[parameter]
        if parameter == 'type':
            message.type = file[parameter]

    return message

# --------------------------------------------------------------------------------------------------------------------


def set_conversation_id(message):
    protocol = message.protocol
    id_extension = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(7))
    if protocol in ['fipa request', 'request interaction protocol',
                    'request protocol', 'fipa request protocol', 'request_interaction_protocol']:
        return fr'RIP-{id_extension}'


    elif protocol in ['fipa request when', 'request when interaction protocol',
                      'request when protocol', 'fipa request-when protocol', 'fipa request when protocol',
                      'request-when protocol']:
        return fr'RWIP-{id_extension}'

    elif protocol in ['fipa propose', 'propose interaction protocol',
                      'propose protocol', 'fipa propose protocol']:
        return fr'PIP-{id_extension}'

    elif protocol in ['fipa subscribe', 'subscribe interaction protocol',
                      'subscribe protocol', 'fipa subscribe protocol']:
        return fr'SIP-{id_extension}'

    elif protocol in ['fipa contract-net', 'contract-net interaction protocol',
                      'contract_net_protocol', 'contract net protocol',
                      'contract_net_interaction_protocol',
                      'fipa contract net protocol',
                      'fipa contract-net protocol', 'contract-net protocol']:
        return fr'CNIP-{id_extension}'

    elif protocol in ['fipa query interaction protocol', 'query_interaction_protocol',
                      'query protocol', 'fipa query protocol']:
        return fr'QIP-{id_extension}'

    elif protocol in ['fipa broking interaction protocol', 'broking_interaction_protocol',
                      'broking protocol', 'fipa broking protocol']:
        return fr'BIP-{id_extension}'

    elif protocol in ['fipa recruiting interaction protocol', 'recruiting_interaction_protocol',
                      'recruiting protocol', 'fipa recruiting protocol']:
        return fr'RecrIP-{id_extension}'


# ---------------------------------------------------------------------------------------------------------------




