import os
import time
import asyncio
import discord
from typing import Final
from dotenv import load_dotenv
from responses import get_response
from discord import Intents, Client, Message, Guild
from discord import app_commands
from discord.ext import commands
from ping import pingall

#load the token from .env
load_dotenv()

#create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

#login with token
def main():
    bot.run(os.getenv("TOKEN"))

#startup
@bot.event
async def on_ready():
    print(f"{bot.user} is now online, may god help us all...")
    #registering slash commands
    await bot.tree.sync()
    
#/ping command
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    print("Pinging CCServer...")
    await interaction.response.send_message(f"{interaction.user.mention} pinged CCServer with the following results:\n{pingall()}")
    
    
    
    
#listen for messages
@bot.event
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

    
        
        
        
