import os
import re
from nickname_rule import *
from mod_tools import kick_member
from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands
from responses import get_response, get_insult
from ping import pingall
from pfp_manipulations import *

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
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    await bot.tree.sync()
    print("Commands synced for all guilds")
    print(f"{bot.user} is now online, may god help us all...")
    
# /ping command
@bot.tree.command(name="ping", description="pings CCServer, please be responsible with this one...")
async def ping(interaction: discord.Interaction):
    await interaction.response.defer()
    print("Pinging CCServer...")
    await interaction.response.send_message(f"{interaction.user.mention} pinged CCServer with the following results:\n{pingall()}")

# /they_call_you command
@bot.tree.command(name = "they_call_you", description = "invokes the rule...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    print(f"attempting to change the nickname of {victim.name} to {new_name}...")
    try:
        await change_nickname(interaction, victim, new_name)
    except Exception as e:
        await interaction.response.send_message(f"Failed to change nickname: {e}")
        
# /set log channel command
@bot.tree.command(name="set_logs_channel", description="where should i spew? (kick/ban messages etc.)")
async def set_logs_channel(interaction: discord.Interaction): 
    print(log_channel_id)
    log_channel_id = bot.get_channel(interaction.channel_id)
    print(log_channel_id)
    await interaction.channel.send(f"{interaction.channel.name} is the new logs channel")
    # maybe something to store in the database, ServerID : LogChannelID ???????????????

# /help command
@bot.tree.command(name="help", description="you dont what to know what i can *really* do...")
async def help(interaction: discord.Interaction): 
    raise NotImplementedError
    
# /kick command
@bot.tree.command(name="kick", description="foekn get 'em yea")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str): 
    await kick_member(interaction, member, reason)

# /boil command, doesnt work if the user has a gif as a pfp
@bot.tree.command(name="boil", description="focken boil yehs")
async def boil(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        await boil_pfp(interaction, victim)
        await interaction.followup.send(f"{victim.mention} has been BOILED!!!")
    except Exception as e:
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to boil {victim.name} but it didnt work :// ({e})")

# /slander command, doesnt work if the user has a gif as a pfp
@bot.tree.command(name="slander", description="i cant belive they said that")
async def slander(interaction: discord.Interaction, victim: discord.Member):
    try:
        await add_speech_bubble(interaction, victim)
         #need the response message to be ephemeral so cant use interaction.followup
        await interaction.response.send_message(content=f"you slandered {victim.name}, they really just said that huh ://", ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message(content=f"{interaction.user.mention} tried to slander {victim.mention}, but it didnt work... ({e})")
 
# /mock command
@bot.tree.command(name="mock", description="cast vicious mockery on someone")
async def mock(interaction: discord.Interaction, victim: discord.Member):
    if victim.id != 1283805971524747304:
        try:
            insult = await get_insult()
            if victim.id == interaction.user.id:
                await interaction.response.send_message(f"{interaction.user.mention} tried to cast Vicious Mockery on themselves for some reason...\nit still works tho, {interaction.user.mention} {insult} ")
            else:
                await interaction.response.send_message(f"{victim.mention} {insult}")
        except Exception as e:
            await interaction.response.send_message(f"{interaction.user.mention} tried to cast Vicious Mockery on {victim.mention}... but it failed ({e})")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} tried to cast Vicious Mockery on me...BITCH")

# test command, change as needed
@bot.tree.command(name="test", description="test command, might do something, might not, who knows")
async def test(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    nicknameprint(victim, new_name)

 
    
    
    
# Message listener
@bot.event
async def on_message(message: Message):
    if not message.author.bot and message.content != "":
        
        inline_commands = [
                                    "<@(.+?)>\s+they\s+call\s+(?:you|u)\s+(.+)"
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
                        await change_nickname(message, victim, newname)
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
