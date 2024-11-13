import os
import re

from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands

from nickname_rule import *
from mod_tools import *
from responses import *
from ping import pingall
from pfp_manipulations import *
from help import *
from json_handling import *
from joker_score import *
from guilds import *


# Load the token from .env
try:
    load_dotenv()
except Exception as e:
    print("Dotenv load failed, either dotenv is not installed or there is no .env file.")
    postgres.log_error(e)

# Create client and intents objects
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
kicked_members = set()
banned_members = set()


def main():
    bot.run(os.getenv("TOKEN"))

# startup
@bot.event
async def on_ready():
    for guild in bot.guilds:
        await bot.tree.sync(guild=guild)
    await bot.tree.sync()
    print("Commands synced for all guilds")
    print(f"{bot.user} is now online, may god help us all...")
    
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# MODERATION
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /kick command
@bot.tree.command(name="kick", description="foekn get 'em yea")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str): 
    if interaction.user.id == member.id:
        await interaction.response.send_message("u cant kick youself idiot, the leave button is right there", ephemeral=True)
        return
    if member.id == bot.user.id:
        await interaction.response.send_message("you cant get rid of me that easily...", ephemeral=True)
        return
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    try:    
        kicked_members.add(member.id)
        channel = await bot.fetch_channel(read_log_channel(interaction.guild.id))
        await channel.send(embed=await kick_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You kicked {member.name}.", ephemeral=True)
        await member.kick(reason=reason)
        print("s")
    except Exception as e:
        print(e)
        postgres.log_error(e)
        await interaction.response.send_message(f"Couldn't kick user {member.name} because {e}", ephemeral=True)

# /ban command 
@bot.tree.command(name="ban", description="KILL! KILL! KILL! KILL!!!!!")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str): 
    if interaction.user.id == member.id:
        await interaction.response.send_message("You can't ban youself idiot, the leave button is right there", ephemeral=True)
        return
    if member.id == bot.user.id:
        await interaction.response.send_message("you cant get rid of me that easily...", ephemeral=True)
        return
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("you really think im gonna let u do that?", ephemeral=True)
        return
    try:
        banned_members.add(member.id)    
        channel = await bot.fetch_channel(read_log_channel(interaction.guild.id))
        await channel.send(embed=await ban_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You banned {member.name}.", ephemeral=True)
        await member.ban(reason=reason)
    except Exception as e:
        print(e)
        postgres.log_error(e)
        await interaction.response.send_message(f"Couldn't ban user {member.name} because {e}", ephemeral=True)

# /mute command
@bot.tree.command(name="mute", description="SHHHHHHHH!!")
async def mute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id == member.id:
        await interaction.response.send_message("mute yourself? just stop talking lol", ephemeral=True)
        return
    if member.id == bot.user.id:
        await interaction.response.send_message("you cant silence me bitch", ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    try:
        await member.edit(mute=True)
    except Exception as e:
        postgres.log_error(e)
        print("Target user is not in a voice channel, consider re-muting if they join.")
    if discord.utils.get(member.guild.roles, name="BeefMute") not in member.roles:
        try:
            await add_mute_role(interaction, member)
            await interaction.response.send_message(f"{member.mention} was muted", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("umm.. no i dont think so")
    else:
        await interaction.response.send_message(f"{member.mention} is already muted", ephemeral=True)

# /unmute command
@bot.tree.command(name="unmute", description="you may speak...")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id == member.id:
        await interaction.response.send_message("mute yourself? just stop talking lol", ephemeral=True)
        return
    if member.id == bot.user.id:
        await interaction.response.send_message("you cant silence me bitch", ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return        
    try:
        await member.edit(mute=False)
    except Exception as e:
        postgres.log_error(e)
        print("Target user is not in a voice channel, consider re-muting if they join.")
    if discord.utils.get(member.guild.roles, name="BeefMute") in member.roles:
        try:
            await remove_mute_role(interaction, member)
            await interaction.response.send_message(f"{member.mention} was unmuted", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("umm.. no i dont think so")
    else:
        await interaction.response.send_message(f"{member.mention} is already unmuted", ephemeral=True)


#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# UTILITIES
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /ping command
@bot.tree.command(name="ccping", description="pings CCServer, please be responsible with this one...")
async def ccping(interaction: discord.Interaction):
    await interaction.response.defer()
    print("Pinging CCServer...")
    await interaction.response.send_message(f"{interaction.user.mention} pinged CCServer with the following results:\n{pingall()}")
        
# /set log channel command
@bot.tree.command(name="set_logs", description="where should i spew? (kick/ban messages etc.)")
async def set_logs(interaction: discord.Interaction):
    await interaction.response.defer()
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if not guild_written(interaction.guild.id): 
        write_guild(interaction.guild.id)
    write_log_channel(interaction.guild.id, interaction.channel.id)
    await interaction.followup.send(f"{interaction.channel.mention} is the new logs channel.", ephemeral=True)

# /set info channel command
@bot.tree.command(name="set_info", description="where should i spew? (kick/ban messages etc.)")
async def set_info(interaction: discord.Interaction):
    await interaction.response.defer()
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if not guild_written(interaction.guild.id): 
        write_guild(interaction.guild.id)
    write_info_channel(interaction.guild.id, interaction.channel.id)
    await interaction.followup.send(f"{interaction.channel.mention} is the new info channel.", ephemeral=True)

# /help command
@bot.tree.command(name="help", description="you dont what to know what i can *really* do...")
async def help(interaction: discord.Interaction):
    view = HelpEmbed()
    page0embed = discord.Embed(title="Beefstew Help", description="You don't want to know what I can *really* do...", color=discord.Color.lighter_grey())
    page0embed.set_thumbnail(url=bot.user.avatar.url)
    page0embed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="Commands:",value="", inline=False)
    page0embed.add_field(name="",value="Click on the buttons below for command lists", inline=False)
    page0embed.add_field(name="",value="⠀", inline=False)
    page0embed.add_field(name="\nOther info:\n",value="", inline=False)
    page0embed.add_field(name="", value="Privacy Policy", inline=True)
    page0embed.add_field(name="", value="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Terms of Service", inline=True)
    page0embed.add_field(name="", value="[cosycraft.uk/privacy](https://www.cosycraft.uk/privacy)⠀⠀⠀⠀⠀⠀⠀[cosycraft/tos](https://www.cosycraft.com/tos)", inline=False)
    await interaction.response.send_message(embed=page0embed, view=view)

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# INVOKATIONS
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /they_call_you command
@bot.tree.command(name = "they_call_you", description = "invokes the rule...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    try:
        await change_nickname(interaction, victim, new_name)
    except Exception as e:
        postgres.log_error(e)
        await interaction.response.send_message(f"Failed to change nickname: {e}")

@bot.tree.command(name= "plus2", description="good one buddy")
async def plus2(interaction: discord.Interaction, joker: discord.Member):
    await interaction.response.defer()
    if not await is_registered(joker):
        await register_user(joker)
    try:
        mult = await get_multilplier(joker)
        await increment_joke_score(joker, 2, mult)
        await interaction.followup.send(await get_joke_response_positive(joker))
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"couldnt +2 {joker.name} :( ({e}))")

@bot.tree.command(name= "minus2", description="*tugs on collar* yikes...")
async def minus2(interaction: discord.Interaction, joker: discord.Member):
    await interaction.response.defer()
    if not await is_registered(joker):
        await register_user(joker)
    try:
        mult = await get_multilplier(joker)
        await increment_joke_score(joker, -2, mult)
        await interaction.followup.send(await get_joke_response_negative(joker))
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"couldnt +2 {joker.name} :( ({e}))")
        
@bot.tree.command(name= "score", description="how funny are you")
async def score(interaction: discord.Interaction, joker: discord.Member):
    await interaction.response.defer()
    if not await is_registered(joker):
        await register_user(joker)
    try:
        score = await retrieve_joke_score(joker)
        await interaction.followup.send(f"{joker.mention}'s joker score: **{score}**!")
    except Exception as e:
        postgres.log_error(e)
        await interaction.followup.send(f"couldnt find {joker.name}'s score :( ({e}))")
        
@bot.command()
async def score_reset(ctx, joker: discord.Member):
    await clear_joke_score(joker)
    print(f"{joker.name} score reset.")

#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# VISAGE
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
 
# /boil command
@bot.tree.command(name="boil", description="focken boil yehs")
async def boil(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        boiled_pfp = await boil_pfp(victim)
        await interaction.channel.send(f"{victim.mention} WAS BOILED!!!!")
        await interaction.followup.send(file=discord.File(fp=boiled_pfp, filename=f"{victim.name} boiled.png"))
        boiled_pfp.close()
    except Exception as e:
        postgres.log_error(e)
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
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(content=f"{interaction.user.mention} tried to slander {victim.mention}, but it didnt work :// ({e})")

#/down the drain command
@bot.tree.command(name="down_the_drain", description="yeah sorry we dropped them in there we cant get them out ://")
async def down_the_drain(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        drain_pfp = await drain_overlay(victim)
        await interaction.channel.send(f"yeah sorry we dropped {victim.mention} in there we cant get them out ://")
        await interaction.followup.send(file=discord.File(fp=drain_pfp, filename=f"{victim.name} dropped down the drain.png"))
        drain_pfp.close()
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to drop {victim.name} down the drain but it didnt work :// ({e})")
 
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# INCANTATIONS
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /mock command
@bot.tree.command(name="mock", description="cast vicious mockery on someone")
async def mock(interaction: discord.Interaction, victim: discord.Member):
    interaction.response.defer()
    interaction.followup.send(vicious_mockery())

# test command, change as needed
@bot.tree.command(name="test", description="test command, might do something, might not, who knows")
async def test(interaction: discord.Interaction, victim: discord.Member):
    await register_user(victim)

# message listener
@bot.event
async def on_message(message: Message):
    if not message.author.bot and message.content != "":
        inline_commands = [
                                    "<@(.+?)>\s+they\s+call\s+(?:you|u)\s+(.+)",
                                    "<@[^>]+>\s*(\+2|plus\s*2)|(\+2|plus\s*2)\s*<@[^>]+>",
                                    "<@[^>]+>\s*(\-2|minus\s*2)|(\-2|minus\s*2)\s*<@[^>]+>"
                                  ]
        
        # Check for inline commands and keep track of which command is being compared
        for index, pattern in enumerate(inline_commands):
            matched_command = re.match(pattern, message.content)
            print(f"{message.content} vs {inline_commands[index]}, {matched_command}")
            if matched_command:
                print("checking expressions")
                if index == 0:
                    # Don't run the command if it's being invoked in a DM
                    if isinstance(message.channel, discord.DMChannel):
                        await message.channel.send("we are literally in DMs rn bro who tf name u trying to change")
                        break
                    # Derives the new name and retrieves the victim user ID from the input string
                    try:
                        victim = message.guild.get_member(int(matched_command.group(1)))
                    except Exception as e:
                        postgres.log_error(e)
                        print(e)
                        await message.channel.send(f"**{message.author.name}** tried to invoked the rule on.... wha... who?")
                        break                            
                    newname = str(matched_command.group(2))
                    # Calls the /they_call_you slash command logic
                    try:
                        await change_nickname(message, victim, newname)
                    except Exception as e:
                        postgres.log_error(e)
                        print(e)
                elif index == 1:
                    if not await is_registered(message.author):
                        await register_user(message.author)
                    try:
                        mult = await get_multilplier(message.author)
                        await increment_joke_score(message.author, 2, mult)
                        await message.channel.send(await get_joke_response_positive(message.author))
                    except Exception as e:
                        postgres.log_error(e)
                        await message.channel.send(f"couldnt +2 {message.author.name} :( ({e}))")
                elif index == 2:
                    return
            # Not an inline command, check the message against a list of possible responses, then reply with that
            else:
                print(f"'{message.content}' is not a command")
                response = str(get_response(message.content))
                if response != "":
                    await message.reply(response)
    await bot.process_commands(message)

# member join event listener
@bot.event
async def on_member_join(member: discord.Member):
     channel = await bot.fetch_channel((read_log_channel(member.guild.id)))
     await channel.send(embed=await join_message_embed(member, bot.user.avatar.url,member.guild.name))

# member leave event listener
@bot.event
async def on_member_remove(member: discord.Member):
    if member.id in kicked_members:
        kicked_members.remove(member.id)
        return
    if member.id in banned_members:
       banned_members.remove(member.id)
       return
    channel = await bot.fetch_channel((read_log_channel(member.guild.id)))
    await channel.send(embed=await leave_message_embed(member, bot.user.avatar.url, member.guild.name))

# message edit event listener
@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return
    channel = await bot.fetch_channel((read_log_channel(before.guild.id)))  # Replace with your log channel ID
    embed = discord.Embed(title="Message Edited", color=discord.Color.yellow())
    embed.add_field(name="",value=f"{after.author.mention} edited a message in {after.channel.mention} - [Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id})", inline=False)
    embed.add_field(name="Original", value=f"```{before.content}```", inline=False)
    embed.add_field(name="Edited", value=f"```{after.content}```", inline=False)
    embed.add_field(name="", value=f"{after.edited_at.strftime('%d/%m/%Y %H:%M')}")
    embed.add_field(name="", value="", inline=False)
    embed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    embed.add_field(name="", value=f"{after.author.guild.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}") 
    await channel.send(embed=embed)

# message delete event listener
@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    channel = await bot.fetch_channel((read_log_channel(message.guild.id)))  # Replace with your log channel ID
    embed = discord.Embed(title="Message Deleted", color=discord.Color.orange())
    embed.add_field(name="",value=f"{message.author.mention}'s message was deleted in {message.channel.mention}", inline=False)
    embed.add_field(name="Message", value=f"```{message.content}```", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.set_author(name="Beefstew", icon_url=bot.user.avatar.url)
    embed.add_field(name="", value=f"{message.author.guild.name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}") 
    await channel.send(embed=embed)

# entrypoint
if __name__ == "__main__":
    main()
