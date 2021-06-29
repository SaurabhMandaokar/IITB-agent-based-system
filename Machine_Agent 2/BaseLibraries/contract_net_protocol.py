import time

from BaseLibraries.support_files import map_performative_type, pointing, function_execution, create_a_reply_to_send, map_and_point
from BaseLibraries.messaging import FIPA_message,flatten
from BaseLibraries.conversation_logging import create_new_log,log_and_end,log_and_continue
import random

def handle_fipa_contract_net_protocol(message, msg_to_send_queue, paths_dictionary):
    performative = message.performative
    if performative in ['cfp', 'call for proposal', 'call-for-proposal', 'call_for_proposal']:
        # create_new_log(message, paths_dictionary)
        executable_function_name = map_and_point(message)
        print(executable_function_name)
        if executable_function_name is not None:
            print('alloted fuction for:', message.type, executable_function_name)
            result_dict = function_execution(executable_function_name, message.type, message.content,paths_dictionary)
            print('function execution results:', result_dict)
            if result_dict:
                reply_parameters = {}
                reply_parameters["reply_performative"] = 'propose'
                reply_parameters["reply_content"] = result_dict['result']
                reply_parameters["reply_type"] = result_dict['performative_type']
                reply = create_a_reply_to_send(message, reply_parameters)
                msg_to_send_queue.put(reply)
                # log_and_continue(reply, paths_dictionary)

            else:
                reply_parameters = {}
                reply_parameters["reply_performative"] = 'reject'
                reply_parameters["reply_content"] = "function had some error"
                reply_parameters["reply_type"] = result_dict['performative_type']
                reply = create_a_reply_to_send(message, reply_parameters)
                msg_to_send_queue.put(reply)

        else:
            reply_parameters = {}
            reply_parameters["reply_performative"] = 'reject'
            reply_parameters["reply_content"] = "problem in mapping and pointing or no function available"
            reply_parameters["reply_type"] = 'rejected to propose'
            reply = create_a_reply_to_send(message, reply_parameters)
            msg_to_send_queue.put(reply)
            # log_and_end(reply,paths_dictionary)
            return

    elif performative == 'refuse':
        # log_and_end(message, paths_dictionary)
        pass

    elif performative == 'propose':
        # log_and_continue(message, paths_dictionary)
        pass

    elif performative in ['reject-proposal', 'reject_proposal']:
        # log_and_end(message, paths_dictionary)
        pass

    elif performative in ['accept proposal', 'accept-proposal','accept_proposal']:
        reply_parameters = {}
        reply_parameters["reply_performative"] = 'inform'
        reply_parameters["reply_content"] = "None"
        reply_parameters["reply_type"] = 'inform-done'
        reply = create_a_reply_to_send(message, reply_parameters)
        msg_to_send_queue.put(reply)
        pass

    elif performative == 'failure':
        # log_and_end(message, paths_dictionary)
        pass

    elif performative == 'inform':
        # log_and_end(message, paths_dictionary)
        pass


    else:
        pass
        # ====================================================================*
        # when performative is not mentioned or you get different tag
        #  ====================================================================*


def handle_all_proposals(proposals_message_list, msg_to_send_queue, paths_dictionary):
    # the messages in proposal_message_list are to be message objects and not other formats
    try:
        executable_function_name = map_and_point(proposals_message_list[0])
        performative_type = proposals_message_list[0].performative
        print(executable_function_name)

        if executable_function_name is not None:
            accepted_proposer = function_execution(executable_function_name, performative_type, proposals_message_list)
            print("accepted proposer:", accepted_proposer)

            for message in proposals_message_list:
                if message.sender == accepted_proposer:
                    reply = FIPA_message()
                    reply.performative = 'accept_proposal'
                    reply.type = 'accept_proposal'
                    reply.receiver = message.sender
                    reply.protocol = message.protocol
                    reply.conversation_id = message.conversation_id
                    reply.content = 'None'
                    msg_to_send_queue.put(reply)

                    # log_and_continue(reply,paths_dictionary)

                else:
                    reply = FIPA_message()
                    reply.performative = 'reject_proposal'
                    reply.type = 'reject_proposal'
                    reply.receiver = message.sender
                    reply.protocol = message.protocol
                    reply.conversation_id = message.conversation_id
                    reply.content = 'None'
                    msg_to_send_queue.put(reply)
                    # log_and_continue(reply, paths_dictionary)

    except:

        if proposals_message_list[0]:
            senders, costs = [], []
            for message in proposals_message_list:
                senders.append(message.sender)
                costs.append(message.content)
            min_cost_index = costs.index(min(costs))
            accepted_proposer = senders[min_cost_index]

            for message in proposals_message_list:
                if message.sender == accepted_proposer:
                    reply = FIPA_message()
                    reply.performative = 'accept_proposal'
                    reply.type = 'accept_proposal'
                    reply.receiver = message.sender
                    reply.protocol = message.protocol
                    reply.conversation_id = message.conversation_id
                    reply.content = 'None'
                    msg_to_send_queue.put(reply)

                else:
                    reply = FIPA_message()
                    reply.performative = 'reject_proposal'
                    reply.type = 'reject_proposal'
                    reply.receiver = message.sender
                    reply.protocol = message.protocol
                    reply.conversation_id = message.conversation_id
                    reply.content = 'None'
                    msg_to_send_queue.put(reply)
                    # log_and_continue(reply, paths_dictionary)

            return

    return

