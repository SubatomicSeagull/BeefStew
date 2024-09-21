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
    elif "deadly dice man" in message_text:
        response = "🎲You my friend... have just made.. an.. unlucky gamble...🎲\nhttps://cdn.discordapp.com/attachments/1185154272170623016/1216308263348605049/17100608047072368967661815628.gif?ex=66ee89d7&is=66ed3857&hm=a331b00d199db639dadec8dfd406cb7bf1027c7d968ffcb532ba6cb5954badd4&"
    elif "preposition" in message_text:
        response = "prepositions\nhttps://www.youtube.com/watch?v=E0Ag0VKJ51Y"
    elif message_text == "reveal the banger":
        response = "https://x.com/blacklung82/status/1602348576331505664"
        
        
    #check for emoji responses
    if "whatsapp" in message_text:
        response = response + "<:whatsapp:1285617179408076902>"
    if "beefstew" in message_text:
        response = response + "<:beefstew:1285630081829437614>"
    if "romulus" in message_text:
        response = response + "<:romulus:1285630098224971786>"
    if "brazil" in message_text:
        response = response + "<:brazil:1286688098297839696>"
    if "elphaba" in message_text:
        response = response + "<:beefhusk:1287094093989679124>"
        
    return response
