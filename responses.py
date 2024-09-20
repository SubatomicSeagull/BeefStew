def get_response(message):
    message_text = str(message).lower()
    response = ""
    
    #check for text responses
    if message_text == "":
        return
    elif message_text == "oye":
        response = "oye."
    elif message_text == "snarf":
        response = "snarf >:("
        
    #check for emoji responses
    if "whatsapp" in message_text:
        response = response + "<:whatsapp:1285617179408076902>"
    if "beefstew" in message_text:
        response = response + "<:beefstew:1285630081829437614>"
    if "romulus" in message_text:
        response = response + "<:romulus:1285630098224971786>"
        
    return response
