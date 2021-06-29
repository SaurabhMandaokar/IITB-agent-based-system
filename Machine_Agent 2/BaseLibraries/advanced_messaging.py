import time
from datetime import datetime
from BaseLibraries.messaging import flatten, unflatten
from BaseLibraries.contract_net_protocol import handle_all_proposals


def check_advanced_communications(message, timed_reply_queue, msg_to_send_queue, paths_dictionary):
    if message.protocol in ['contract_net_interaction_protocol',
                            'contract_net_protocol'] and message.performative == 'call_for_proposal':
        print("inside advanced cfp")
        recent_messages = []
        t_init = datetime.now()
        all_proposals = []
        time.sleep(5) # the time for which the cfp sender wants to wait for all proposals
        print(timed_reply_queue.queue)
        while not timed_reply_queue.empty():
            print("inside queue filler")
            msg = timed_reply_queue.get()
            recent_messages.append(msg)

        for msg in recent_messages:
            if msg.protocol == 'contract_net_interaction_protocol' and msg.performative == 'propose' and msg.conversation_id == message.conversation_id:
                print("appending message", msg.conversation_id, msg.content)
                all_proposals.append(msg)
            else:
                print("conversation id is not proper", msg.conversation_id, msg.content)
                timed_reply_queue.put(msg)
        print("*****************sending_proposals to executor*********************")
        handle_all_proposals(all_proposals, msg_to_send_queue, paths_dictionary)

