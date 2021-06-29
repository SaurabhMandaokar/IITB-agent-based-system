

def handle_fipa_broking_protocol(message):
    # ---------------------------------------------------------
    #   FIPA BROKING PROTOCOL IS UNDER DEVELOPMENT (incomplete)
    # ---------------------------------------------------------

    performative = message.performative
    if performative == 'proxy':
        pass

    elif performative == 'refuse':
        # -------------------------------------------
        #   broker refuses to proxy the interaction
        # -------------------------------------------
        pass

    elif performative == 'agree':
        # -------------------------------------------
        #   broker agrees to proxy the interaction
        # -------------------------------------------
        pass

    elif performative == 'failure':
        # -------------------------------------------------------------
        #   there are three failure conditions here
        #       1. failure - no match (agreed but cannot find the target agents)
        #       2. failure-proxy (unable to connect to agents)
        #       3. failure (result of interaction)
        # -------------------------------------------
        pass

    elif performative == 'inform':
        pass

    else:
        pass
        # ====================================================================*
        # when performative is not mentioned or you get diffrent tag
        #  ====================================================================*
