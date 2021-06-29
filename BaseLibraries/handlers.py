import json
import pickle
from BaseLibraries.messaging import *
from BaseLibraries.support_files import *

from BaseLibraries.request_interaction_protocol import handle_fipa_request_protocol
from BaseLibraries.request_when_protocol import handle_fipa_request_when_protocol
from BaseLibraries.broking_interaction_protocol import handle_fipa_broking_protocol
from BaseLibraries.contract_net_protocol import handle_fipa_contract_net_protocol
from BaseLibraries.propose_protocol import handle_fipa_propose_protocol
from BaseLibraries.subscribe_protocol import handle_fipa_subscribe_protocol
from BaseLibraries.query_protocol import handle_fipa_query_protocol
from BaseLibraries.recruiting_interaction_protocol import handle_fipa_recruiting_protocol

# -------------------------------------------------------------------------------------------------*
# #messages transfer takes place as follows:
#  *At sender end*
#       1. the message object is created and details are filled
#       2. Message object converted to JSON
#       3. JSON is serialised and ready to send via TCP
#
#  $ at receiver end $
#       1. message unserialised to JSON
#         2. JSON message converted to message object
#         3. message object is used for further processing
# ------------------------------------------------------------------------------------------------*


# --------------------------------------------------------------------------------------------------------*
# #                                 list of all Protocols and performatives  |
# ---------------------------------------------------------------------------------------------------------*
# protocols = ['request interaction protocol', 'request-when interaction protocol', 'query interaction protocol',
#              'contract-net interaction protocol', 'broking interaction protocol', 'recruiting interaction protocol',
#              'propose interaction protocol', 'subscribe interaction protocol']
#
# performatives = ['accept-proposal', 'agree', 'cancel', 'cfp', 'confirm',
#                  'disconfirm',' failure', 'inform', 'inform-if', 'inform-ref'
#                  ,'not understood','propagate', 'propose', 'proxy', 'query-if',
#                  'query-ref', 'refuse', 'reject-proposal', 'request', 'request-when'
#                  'request-whenever', 'subscribe']

# --------------------------------------------------------------------------------------------------------*
# #         identifying the protocol from the message object created from the recieved |
# ---------------------------------------------------------------------------------------------------------*


def message_handler(message, msg_to_send_queue, paths_dictionary,allotment_queue):
    protocol = message.protocol
    if protocol in ['fipa request', 'request interaction protocol',
                    'request protocol', 'fipa request protocol', 'request_interaction_protocol']:
        reply_parameters = handle_fipa_request_protocol(message, msg_to_send_queue, paths_dictionary)

    elif protocol in ['fipa request when', 'request when interaction protocol',
                      'request when protocol', 'fipa request-when protocol', 'fipa request when protocol',
                      'request-when protocol']:
        handle_fipa_request_when_protocol(message, msg_to_send_queue, paths_dictionary)

    elif protocol in ['fipa propose', 'propose interaction protocol',
                      'propose protocol', 'fipa propose protocol']:
        handle_fipa_propose_protocol(message)

    elif protocol in ['fipa subscribe', 'subscribe interaction protocol',
                      'subscribe protocol', 'fipa subscribe protocol']:
        handle_fipa_subscribe_protocol(message)

    elif protocol in ['fipa contract-net', 'contract-net interaction protocol',
                      'contract_net_protocol', 'contract net protocol',
                      'contract_net_interaction_protocol',
                      'fipa contract net protocol',
                      'fipa contract-net protocol', 'contract-net protocol']:
        handle_fipa_contract_net_protocol(message, msg_to_send_queue, paths_dictionary,allotment_queue)

    elif protocol in ['fipa query interaction protocol', 'query interaction protocol',
                      'query protocol', 'fipa query protocol']:
        handle_fipa_query_protocol(message)

    elif protocol in ['fipa broking interaction protocol', 'broking interaction protocol',
                      'broking protocol', 'fipa broking protocol']:
        handle_fipa_broking_protocol(message)

    elif protocol in ['fipa recruiting interaction protocol', 'recruiting interaction protocol',
                      'recruiting protocol', 'fipa recruiting protocol']:
        handle_fipa_recruiting_protocol(message)

    elif message.performative =='not_understood':
        pass

    else:
        reply_parameters = {}
        reply_parameters['reply_performative'] = 'not_understood'
        reply_parameters['reply_content'] = "protocol mentioned is not understood"
        reply_parameters['reply_type'] = None
        reply = create_a_reply_to_send(message, reply_parameters)
        msg_to_send_queue.put(reply)

    return








