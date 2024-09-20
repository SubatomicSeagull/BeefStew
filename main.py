from discord import Intents, Client, Message, Guild
import os
import time
import asyncio
from typing import Final
from dotenv import load_dotenv
from responses import get_response

#load the token from .env
load_dotenv()
TOKEN: Final[str] = os.getenv("TOKEN")

#create client and intents objects
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#login with token
def main():
    client.run(token=TOKEN)

#startup
@client.event
async def on_ready():
    print(f"{client.user} is now online, may god help us all...")
    
#listen for messages
@client.event
async def on_message(message: Message):
    #sends a message if the message is not empty and not sent by a bot
    if not message.author.bot and message.content != "":
        response = str(get_response(message.content))
        #print(f"response: {response}")
        if response != "":
            await message.reply(response)
                
#entrypoint     
if __name__ == "__main__":
    main()

    
        
        
        
