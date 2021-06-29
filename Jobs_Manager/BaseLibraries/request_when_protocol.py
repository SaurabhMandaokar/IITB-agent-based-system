from BaseLibraries.conversation_logging import create_new_log, log_and_continue, log_and_end
from BaseLibraries.support_files import map_performative_type, pointing, function_execution, create_a_reply_to_send, map_and_point
from BaseLibraries.messaging import FIPA_message,flatten


def handle_fipa_request_when_protocol(message, msg_to_send_queue, paths_dictionary):


    performative = message.performative
    print(performative, type(performative))
    if performative in ['request_when', "request-when"]:
        create_new_log(message, paths_dictionary)
        executable_function_name = map_and_point(message)
        print(executable_function_name)
        if executable_function_name is not None:
            reply_parameters = {}
            reply_parameters["reply_performative"] = 'agree'
            reply_parameters["reply_content"] = "None"
            reply_parameters["reply_type"] = 'agree'
            reply = create_a_reply_to_send(message, reply_parameters)
            if reply is not None:
                msg_to_send_queue.put(reply)
                log_and_continue(reply, paths_dictionary)

                result_to_inform = function_execution(executable_function_name, message.content)
                print(result_to_inform)
                reply_parameters = {}
                reply_parameters["reply_performative"] = 'inform'
                reply_parameters["reply_content"] = result_to_inform
                reply_parameters["reply_type"] = 'inform_result'
                reply = create_a_reply_to_send(message, reply_parameters)
                msg_to_send_queue.put(reply)
                log_and_end(reply, paths_dictionary)


            else:
                reply_parameters = {}
                reply_parameters["reply_performative"] = 'refuse'
                reply_parameters["reply_content"] = "refused - cause will be mentioned here"
                reply_parameters["reply_type"] = 'refuse'
                reply = create_a_reply_to_send(message, reply_parameters)
                msg_to_send_queue.put(reply)
                log_and_end(reply, paths_dictionary)

        else:
            reply_parameters = {}
            reply_parameters["reply_performative"] = 'refuse'
            reply_parameters["reply_content"] = "problem in mapping and pointing"
            reply_parameters["reply_type"] = 'refuse'
            reply = create_a_reply_to_send(message, reply_parameters)
            msg_to_send_queue.put(reply)
            log_and_end(reply, paths_dictionary)
            return


    elif performative == 'refuse':
        log_and_end(message, paths_dictionary)
        return

    elif performative == 'agree':
        log_and_continue(message, paths_dictionary)
        return

    elif performative == 'failure':
        log_and_end(message, paths_dictionary)
        return

    elif performative == 'inform':
        log_and_end(message, paths_dictionary)
        return

    elif performative in ['not_understood', 'not understood']:
        log_and_end(message, paths_dictionary)
        return

    else:
        reply_parameters = {}
        reply_parameters["reply_performative"] = 'not_understood'
        reply_parameters["reply_content"] = "performative mentioned is out of conversation flow"
        reply_parameters["reply_type"] = "None"
        reply = create_a_reply_to_send(message, reply_parameters)
        msg_to_send_queue.put(reply)
        return

    return