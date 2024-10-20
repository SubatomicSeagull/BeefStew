import os
import re
from nickname_rule import *
from mod_tools import *
from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands
from responses import get_response, vicious_mockery
from ping import pingall
from pfp_manipulations import *
from help import *

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
@bot.tree.command(name="ccping", description="pings CCServer, please be responsible with this one...")
async def ccping(interaction: discord.Interaction):
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
        interaction.response.is_done(True)
        
# /set log channel command
@bot.tree.command(name="logs", description="where should i spew? (kick/ban messages etc.)")
async def logs(interaction: discord.Interaction):
    await interaction.response.defer()
    
    current_guild_id = read_guild_id()
    current_channel_id = read_log_channel(current_guild_id)
    
    new_guild_id = interaction.guild_id
    new_channel_id = interaction.channel_id
    
    current_channel = await bot.fetch_channel(current_channel_id)
    new_channel = await bot.fetch_channel(new_channel_id)
    try:
        await write_guild_id(new_guild_id, new_channel_id)
        await interaction.followup.send(f"Log channel has been set to {new_channel.mention}")
    except Exception as e:
        print(e)
        await interaction.followup.send(f"Couldn't set the log channel here: {e}. The current log channel is {current_channel.mention}")


# /help command
@bot.tree.command(name="help", description="you dont what to know what i can *really* do...")
async def help(interaction: discord.Interaction): 
    view = HelpEmbed()
    page0embed = discord.Embed(title="Beefstew Help", description="You don't want to know what I can *really* do...", color=discord.Color.lighter_grey())
    page0embed.set_thumbnail(url=bot.user.avatar.url)
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="Commands:",value="", inline=False)
    page0embed.add_field(name="",value="Click on the buttons below for command lists", inline=False)
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="\nOther info:\n",value="", inline=False)
    page0embed.add_field(name="", value="Privacy Policy", inline=True)
    page0embed.add_field(name="", value="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Terms of Service", inline=True)
    page0embed.add_field(name="", value="[cosycraft.uk/privacy](https://www.cosycraft.uk/privacy)⠀⠀⠀⠀⠀⠀⠀[cosycraft/tos](https://www.cosycraft.com/tos)", inline=False)
    await interaction.response.send_message(embed=page0embed, view=view)

# /kick command
@bot.tree.command(name="kick", description="foekn get 'em yea")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str): 
    await kick_member(interaction, member, reason)

# /boil command
@bot.tree.command(name="boil", description="focken boil yehs")
async def boil(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        boiled_pfp = await boil_pfp(victim)
        await interaction.followup.send(file=discord.File(fp=boiled_pfp, filename=f"{victim.name} boiled.png"))
        boiled_pfp.close()
    except Exception as e:
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to boil {victim.name} but it didnt work :// ({e})")

# /slander command
@bot.tree.command(name="slander", description="i cant belive they said that")
async def slander(interaction: discord.Interaction, victim: discord.Member):   
    await interaction.response.defer()
    try:
        slandered_pfp = await add_speech_bubble(victim)
        await interaction.followup.send(file=discord.File(fp=slandered_pfp, filename=f"{victim.name} slandered.png"))
        slandered_pfp.close()
    except Exception as e:
        print(e)
        await interaction.followup.send(content=f"{interaction.user.mention} tried to slander {victim.mention}, but it didnt work :// ({e})")
 
# /mock command
@bot.tree.command(name="mock", description="cast vicious mockery on someone")
async def mock(interaction: discord.Interaction, victim: discord.Member):
    interaction.response.defer()
    interaction.channel.send(vicious_mockery())

# test command, change as needed
@bot.tree.command(name="test", description="test command, might do something, might not, who knows")
async def test(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    nicknameprint(victim, new_name)
    
@bot.tree.command(name="hello", description="test command, might do something, might not, who knows")
async def hello(interaction: discord.Interaction):
    await interaction.channel.send("Hello with prefix command!")

 
    
    
    
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
    await bot.process_commands(message)
# Entrypoint
if __name__ == "__main__":
    main()
