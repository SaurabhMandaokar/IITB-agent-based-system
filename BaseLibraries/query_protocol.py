def handle_fipa_query_protocol(message):
    performative = message.performative
    if performative in ['query-if', 'query if']:
        pass

    elif performative in ['query-ref', 'query ref']:
        pass

    elif performative == 'agree':
        pass

    elif performative == 'refuse':
        pass

    elif performative == 'failure':
        pass

    elif performative == 'inform':
        pass

    else:
        pass
        # ====================================================================*
        # when performative is not mentioned or you get diffrent tag
        #  ====================================================================*
