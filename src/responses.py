def get_response(message):
    message_text = str(message).lower()
    if not message_text:
        return ""

    # Dictionary for text responses
    text_responses = {
        "oye": "oye.",
        "snarf": "snarf >:(",
        "reveal the banger": "https://x.com/blacklung82/status/1602348576331505664"
    }

    # Dictionary for keyword responses
    keyword_responses = {
        "deadly dice man": "🎲You my friend... have just made.. an.. unlucky gamble...🎲\nhttps://cdn.discordapp.com/attachments/1185154272170623016/1216308263348605049/17100608047072368967661815628.gif?ex=66ee89d7&is=66ed3857&hm=a331b00d199db639dadec8dfd406cb7bf1027c7d968ffcb532ba6cb5954badd4&",
        "preposition": "prepositions\nhttps://www.youtube.com/watch?v=E0Ag0VKJ51Y"
    }

    # Dictionary for emoji responses
    emoji_responses = {
        "whatsapp": "<:whatsapp:1285617179408076902>",
        "beefstew": "<:beefstew:1285630081829437614>",
        "romulus": "<:romulus:1285630098224971786>",
        "brazil": "<:brazil:1286688098297839696>",
        "elphaba": "<:beefhusk:1287094093989679124>"
    }

    response = ""

    # Check for exact text responses
    if message_text in text_responses:
        response += text_responses[message_text]

    # Check for keyword responses
    for keyword, keyword_response in keyword_responses.items():
        if keyword in message_text:
            response += keyword_response
            break

    # Append emoji responses in order of appearance
    for word in message_text.split():
        if word in emoji_responses:
            response += emoji_responses[word]

    return response
