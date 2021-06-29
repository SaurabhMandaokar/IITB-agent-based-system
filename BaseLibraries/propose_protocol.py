def handle_fipa_propose_protocol(message):
    performative = message.performative
    if performative == 'propose':
        reply_performative = 'accept-proposal'
        reply_content = 'propose message received, sending accept-proposal'
        reply_type = "some_type"

    elif performative in ['reject-proposal', 'reject proposal']:
        pass

    elif performative == 'accept-proposal':
        pass

    else:
        pass
        # ====================================================================*
        # when performative is not mentioned or you get diffrent tag
        #  ====================================================================*
