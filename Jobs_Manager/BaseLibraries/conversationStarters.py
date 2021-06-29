from BaseLibraries.messaging import FIPA_message, set_conversation_id


def conversation_starter(protocol, performative, performative_type, content, msg_to_send_queue):
    msg = FIPA_message()
    msg.protocol = protocol
    msg.performative = performative
    msg.type = performative_type
    msg.content = content
    msg.receiver = '2'
    msg.conversation_id = set_conversation_id(msg)
    msg_to_send_queue.put(msg)
