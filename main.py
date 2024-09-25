import os
import time
import asyncio
import re
from typing import Final

#external libraries
from dotenv import load_dotenv

#discord libraries
import discord
from discord import Intents, Client, Message, Guild
from discord import app_commands
from discord.ext import commands

#internal functions
from responses import get_response
from ping import pingall
from nicknamerule import nicknameprint

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
    
# "they call you slash" command
@bot.tree.command(name="they_call_you", description="They call you...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, newname: str):
    await nicknamerule(interaction, victim, newname)

#nickname rule, handles logic for they call you slash command
async def nicknamerule(interaction: discord.Interaction, victim: discord.Member, newname: str):
    # not allowed to rename the bot
    if victim.id != 1283805971524747304:
    # not allowed to rename yourself
        if victim.id == interaction.user.id:
            await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
        else:
            try:
                await victim.edit(nick=newname)
                await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.name}**!\n{nicknameprint(interaction, victim, newname)}")           
            except Exception as e:
                print(e)
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
    else:
        # missing permissions
        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")


#checks the message reply against a list of possible commands by matching the pattern
def replyresponse(message: discord.Message):
    replyto = message.channel.fetch_message(message.reference.message_id)

#listen for messages
@bot.event
async def on_message(message: Message):
    #sends a message if the message is not empty and not sent by a bot
    if not message.author.bot and message.content != "":
        #if the message is a reply
        if message.reference:
            #get the username of the person being replied to
            replyto = await message.channel.fetch_message(message.reference.message_id)
  
        #check the message against a list of possible responses, then reply with that
        else:
            inline_commands = [
                                    "<@(.+?)>\s+they\s+call\s+you\s+(.+)"
                                  ]
                #check for inline commands
            for pattern in inline_commands:

                match = re.match(pattern, message.content)
                if match:
                    #derives the new name and retrives the victin user ID from the input string
                    victim = message.guild.get_member(int(match.group(1)))
                    newname = str(match.groups(2))
                    #calls the /they_call_you slash command
                    try:

                        # wont work because it expects an interaction object and a message object is given
                        #could replace interation.message.send with guild.channel.send if we can find the guild info.
                        await nicknamerule(message, victim, newname)
                    except Exception as e:
                        print(e)
                else:
                    response = str(get_response(message.content))
                    if response != "":
                        await message.reply(response)
                
#entrypoint     
if __name__ == "__main__":
    main()

    
        
        
        
