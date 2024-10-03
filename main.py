#general
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
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")

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
    # registering slash commands
    await bot.tree.sync()
    
#/ping command
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    print("Pinging CCServer...")
    await interaction.response.send_message(f"{interaction.user.mention} pinged CCServer with the following results:\n{pingall()}")
    
#/they_call_you" command
@bot.tree.command(name="they_call_you", description="They call you...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, newname: str):
    await nicknamerule(interaction, victim, newname)

#nickname rule, handles logic for they call you slash command
async def nicknamerule(intormessage, victim: discord.Member, newname: str):
    #checks to see if the interaction is through an interaction object or a message object, effectivly switches between using the slash command and having the command run inline
        if isinstance(intormessage, discord.Interaction):
            interaction = intormessage
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == interaction.user.id:
                    await interaction.response.send_message(f"**{interaction.user.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=newname)
                        await interaction.response.send_message(f"**{interaction.user.name}** invoked the rule on **{victim.name}**!\n{nicknameprint(victim, newname)}")           
                    except Exception as e:
                        print(e)
                        await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await interaction.response.send_message(f"**{interaction.user.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")
                
        elif isinstance(intormessage, discord.Message):
            message = intormessage
            # not allowed to rename the bot
            if victim.id != 1283805971524747304:
                # not allowed to rename yourself
                if victim.id == message.author.id:
                    await message.channel.send(f"**{message.author.name}** tried to invoke the rule on themselves... for some reason")
                else:
                    try:
                        await victim.edit(nick=newname)
                        await message.channel.send(f"**{message.author.name}** invoked the rule on **{victim.name}**!\n{nicknameprint(victim, newname)}")
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nbut it didnt work :( next time get some permissions okay?")
            else:
                await message.channel.send(f"**{message.author.name}** tried to invoked the rule on **{victim.name}**!\nnice try fucker...")


#message listener
@bot.event
async def on_message(message: Message):
    if not message.author.bot and message.content != "":
        
        inline_commands = [
                                    "<@(.+?)>\s+they\s+call\s+(?:you|u)\s+(.+)"
                                  ]
        
        #check for inline commands and keep track of which command is being compared
        for index, pattern in enumerate(inline_commands):
            matchedcommand = re.match(pattern, message.content)
            if matchedcommand:
                if index == 0:
                    #dont run the command if its being invoked in a DM
                    if isinstance(message.channel, discord.DMChannel):
                        await message.channel.send("we are literally in DMs rn bro who tf name u trying to change")
                        break
                    #derives the new name and retrieves the victim user ID from the input string
                    try:
                        if not victim in message.guild.members:
                            await message.channel.send(f"**{message.author.name}** tried to invoked the rule on.... wha... who?")
                            break
                        victim = message.guild.get_member(int(matchedcommand.group(1)))
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on.... wha... who?")
                        break                            
                    newname = str(matchedcommand.group(2))
                    #calls the /they_call_you slash command logic
                    try:
                        await nicknamerule(message, victim, newname)
                    except Exception as e:
                        print(e)
                #elif index == 1:
        
            #not an inline command, check the message against a list of possible responses, then reply with that
            else:
                response = str(get_response(message.content))
                if response != "":
                    await message.reply(response)

#entrypoint     
if __name__ == "__main__":
    main()

    
        
        
        
