import os
import re
from nickname_rule import *
from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands
from responses import get_response
from ping import pingall

# Load the token from .env
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")

# Create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Login with token
def main():
    bot.run(os.getenv("TOKEN"))

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} is now online, may god help us all...")
    # Registering slash commands
    await bot.tree.sync()

# /ping command
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    print("Pinging CCServer...")
    await interaction.response.send_message(f"{interaction.user.mention} pinged CCServer with the following results:\n{pingall()}")

# /they_call_you command
@bot.tree.command(name = "they_call_you", description = "They call you...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    try:
        await change_nickname(interaction, victim, new_name)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Failed to change nickname: {e}")

# Message listener
@bot.event
async def on_message(message: Message):
    if not message.author.bot and message.content != "":
        
        inline_commands = [
                                    r"<@(.+?)>\s+they\s+call\s+(?:you|u)\s+(.+)"
                                  ]
        
        # Check for inline commands and keep track of which command is being compared
        for index, pattern in enumerate(inline_commands):
            matched_command = re.match(pattern, message.content)
            if matched_command:
                if index == 0:
                    # Don't run the command if it's being invoked in a DM
                    if isinstance(message.channel, discord.DMChannel):
                        await message.channel.send("we are literally in DMs rn bro who tf name u trying to change")
                        break
                    # Derives the new name and retrieves the victim user ID from the input string
                    try:
                        victim = message.guild.get_member(int(matched_command.group(1)))
                    except Exception as e:
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on.... wha... who?")
                        break                            
                    newname = str(matched_command.group(2))
                    # Calls the /they_call_you slash command logic
                    try:
                        await they_call_you(message, victim, newname)
                    except Exception as e:
                        print(e)
                # elif index == 1:
        
            # Not an inline command, check the message against a list of possible responses, then reply with that
            else:
                response = str(get_response(message.content))
                if response != "":
                    await message.reply(response)

# Entrypoint
if __name__ == "__main__":
    main()
