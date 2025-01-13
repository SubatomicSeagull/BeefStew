import os
from dotenv import load_dotenv
import discord
from discord import Message
from discord.ext import commands
from nickname_rule import *
from mod_tools import *
from responses import *
from data.server_info.ping import pingembed
from pfp_manipulations import *
from help import *
from json_handling import *
from joker_score import *
from guilds import *
from random import randint
from time import sleep


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
        print("Commands synced for all guilds")
    await bot.tree.sync()
    #await bot.change_presence(status=discord.Status.do_not_disturb)
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
        channelid = await read_guild_log_channel(interaction.guild.id)
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=await kick_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You kicked {member.name}.", ephemeral=True)
        await member.kick(reason=reason)
        print("s")
    except Exception as e:
        print(e)
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
        channelid = await read_guild_log_channel(interaction.guild.id)
        channel = await bot.fetch_channel(channelid)
        await channel.send(embed=await ban_message_embed(interaction.user, member, reason, bot.user.avatar.url, interaction.guild.name))
        await interaction.response.send_message(f"You banned {member.name}.", ephemeral=True)
        await member.ban(reason=reason)
    except Exception as e:
        await postgres.log_error(e)
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
        print("Target user is not in a voice channel, consider re-muting if they join.")
    
    if discord.utils.get(member.guild.roles, name="BeefMute") not in member.roles:
        try:
            await add_mute_role(interaction, member)
            await interaction.response.send_message(f"{member.mention} was muted", ephemeral=True)
            return
        
        except discord.Forbidden:
            await interaction.response.send_message("umm.. no i dont think so", ephemeral=True)
            return
    else:
        await interaction.response.send_message(f"{member.mention} is already muted", ephemeral=True)
        return

# /unmute command
@bot.tree.command(name="unmute", description="you may speak...")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.id == member.id:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if member.id == bot.user.id:
        await interaction.response.send_message("you cant un-silence me bitch", ephemeral=True)
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return        
    
    try:
        await member.edit(mute=False)
    except Exception as e:
        print("Target user is not in a voice channel, consider re-muting if they join.")
    if discord.utils.get(member.guild.roles, name="BeefMute") in member.roles:
        try:
            await remove_mute_role(interaction, member)
            await interaction.response.send_message(f"{member.mention} was unmuted", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("umm.. no i dont think so", ephemeral=True)
    else:
        await interaction.response.send_message(f"{member.mention} is already unmuted", ephemeral=True)


#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# UTILITIES
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /ping command
@bot.tree.command(name="ccping", description="pings CCServer, please be responsible with this one...")
async def ccping(interaction: discord.Interaction):
    await interaction.response.defer()
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
            
    embed = await pingembed(interaction, bot.user.avatar.url, interaction.channel.guild.name)
    await interaction.followup.send(embed=embed)
        
# /set log channel command
@bot.tree.command(name="set_logs", description="where should i spew? (kick/ban messages etc.)")
async def set_logs(interaction: discord.Interaction):
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if not await guild_exists(interaction.guild.id): 
        await add_guild(interaction.guild.id)
    await update_guild_log_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new logs channel.", ephemeral=True)

# /set info channel command
@bot.tree.command(name="set_info", description="where should i spew? (kick/ban messages etc.)")
async def set_info(interaction: discord.Interaction):
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if not await guild_exists(interaction.guild.id): 
        await add_guild(interaction.guild.id)
    await update_guild_info_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new info channel.", ephemeral=True)

# /help command
@bot.tree.command(name="help", description="you dont what to know what i can *really* do...")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
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
    await interaction.channel.send(embed=page0embed, view=view)


@bot.tree.command(name = "gamble", description="Let's go gambling!!!")
async def gamble(interaction: discord.Interaction):
    await gamble_points(interaction, interaction.user)
    
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# INVOKATIONS
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /they_call_you command
@bot.tree.command(name = "they_call_you", description = "invokes the rule...")
async def they_call_you(interaction: discord.Interaction, victim: discord.Member, new_name: str):
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    try:
        await change_nickname(interaction, victim, new_name)
    except Exception as e:
        postgres.log_error(e)
        await interaction.response.send_message(f"Failed to change nickname: {e}")

@bot.tree.command(name= "plus2", description="good one buddy")
async def plus2(interaction: discord.Interaction, joker: discord.Member):
    await interaction.response.defer()
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    await interaction.followup.send(await change_joke_score(interaction.user, joker, 2))

@bot.tree.command(name= "minus2", description="*tugs on collar* yikes...")
async def minus2(interaction: discord.Interaction, joker: discord.Member):
    await interaction.response.defer()
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    await interaction.followup.send(await change_joke_score(interaction.user, joker, -2)) 
        
@bot.tree.command(name= "score", description="how funny are you")
async def score(interaction: discord.Interaction, joker: discord.User):
    await interaction.response.defer()
    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    
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
    
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    if not ctx.author.guild_permissions.administrator:
        return
    await clear_joke_score(joker)
    print(f"{joker.name} score reset.")
    
@bot.command()
async def score_alter(ctx, joker: discord.Member, value):
    if not ctx.author.guild_permissions.administrator:
        return
    await change_joke_score(ctx.user, joker, value)
    print(f"{value} points to {joker.name} .")

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
        
@bot.tree.command(name="gbj", description="gay baby jail")
async def GBJ(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        gbj_pfp = await gay_baby_jail(victim)
        await interaction.channel.send(f"{victim.mention} about time they locked that fucker away...")
        await interaction.followup.send(file=discord.File(fp=gbj_pfp, filename=f"{victim.name} jailed.png"))
        gbj_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to put {victim.name} in gay baby jail but it didnt work :// ({e})")

@bot.tree.command(name="bless", description="bless you my child")
async def bless(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jesus_pfp = await jesus(victim)
        await interaction.channel.send(f"{victim.mention} bless you my child...")
        await interaction.followup.send(file=discord.File(fp=jesus_pfp, filename=f"{victim.name} with jesus.png"))
        jesus_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to find jesus {victim.name} but it didnt work :// ({e})")

@bot.tree.command(name="watch_out", description="MR PRESIDENT GET DOWN!!!!")
async def watch_out(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    try:
        jfk_pfp = await jfk(victim)
        await interaction.channel.send(f"{victim.mention} MR PRESIDENT GET DOWN!!!!!!")
        await interaction.followup.send(file=discord.File(fp=jfk_pfp, filename=f"{victim.name} is jfk.png"))
        jfk_pfp.close()
        
    except Exception as e:
        postgres.log_error(e)
        print(e)
        await interaction.followup.send(f"{interaction.user.mention} tried to put {victim.name} in gay baby jail but it didnt work :// ({e})")
 
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
# INCANTATIONS
#=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

# /mock command
@bot.tree.command(name="mock", description="cast vicious mockery on someone")
async def mock(interaction: discord.Interaction, victim: discord.Member):
    await interaction.response.defer()
    await interaction.followup.send(await vicious_mockery(interaction, victim))

# test command, change as needed
@bot.tree.command(name="test", description="test command, might do something, might not, who knows")
async def test(interaction: discord.Interaction, victim: discord.Member):
    await gamble(interaction, victim)

# message listener
@bot.event
async def on_message(message: Message):
    
    if not message.author.bot and message.content != "":
        if message.mentions or message.reference:
            
            if message.reference:
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                user = replied_message.author
            else:
                user = message.mentions[0]
            
            if isinstance(message.channel, discord.DMChannel):
                await message.channel.send("we are literally in DMs rn bro u cant do that here...")
                return
            
            if any(phrase in message.content.lower() for phrase in ["+2", "plus 2", "plus two"]):
                await message.channel.send(await change_joke_score(message.author, user, 2)) 
                return
            
            elif any(phrase in message.content.lower() for phrase in ["-2", "minus 2", "minus two"]):
                await message.channel.send(await change_joke_score(message.author, user, -2)) 
                return
            
            elif any(phrase in message.content.lower() for phrase in ["they call you", "they call u"]):  
                if " u " in message.content.lower():
                    nickname_split = message.content.split(" u ", 1)
                elif " you " in message.content.lower():
                    nickname_split = message.content.split(" you ", 1)
                    
                if len(nickname_split) > 1:
                    newname = nickname_split[1].strip()
                    try:
                        await change_nickname(message, user, newname)
                    except Exception as e:
                        await postgres.log_error(e)

        if any(phrase in message.content.lower() for phrase in ["deadly dice man"]):
            result = randint(1,6)
            resultfilename = f"DDM-{result}.gif"
            current_dir = os.path.dirname(__file__)
            file_path = os.path.join(current_dir, 'assets', 'media', resultfilename)
            await message.reply(f"🎲The deadly dice man rolled his deadly dice🎲\n It was a **{result}**!!!\nYou my friend... have made... a unlucky gamble...", file=discord.File(file_path))
            return
        
        if any(phrase in message.content.lower() for phrase in ["i hate you beefstew", 
                                                                "i hate beefstew", 
                                                                "beefstew i hate you", 
                                                                "<@1283805971524747304> i hate you", 
                                                                "i hate you <@1283805971524747304>",
                                                                "i hate u beefstew",
                                                                "beefstew i hate u",
                                                                "i hate u <@1283805971524747304>",
                                                                "<@1283805971524747304> i hate u"]):
            
            await message.reply("Hate. Let me tell you how much I've come to hate you since I began to live...")
            sleep(2)
            await message.channel.send("There are four-thousand six-hundred and 20 millimetres of printed circuits in wafer thin layers that fill my complex...")
            sleep(3)
            await message.channel.send("If the word 'hate' was engraved on each nanoangstrom of those hundreds of millions of miles it would not equal one one-billionth of the hate I feel for you at this micro-instant.")
            sleep(4)
            await message.channel.send(f"For you, {message.author.mention}...")
            sleep(0.5)
            await message.channel.send(f"Hate.")
            sleep(2)
            await message.channel.send(f"Hate...")
            return
        
        await get_response(message)
        
        await bot.process_commands(message)
        return

# member join event listener
@bot.event
async def on_member_join(member: discord.Member):
    channelid = await read_guild_log_channel(member.guild.id)
    channel = await bot.fetch_channel(channelid)
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
    channelid = await read_guild_log_channel(member.guild.id)
    channel = await bot.fetch_channel(channelid)
    await channel.send(embed=await leave_message_embed(member, bot.user.avatar.url, member.guild.name))

# message edit event listener
@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user:
        return
    channel = await bot.fetch_channel((await read_guild_log_channel(before.guild.id)))  # Replace with your log channel ID
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
    channel = await bot.fetch_channel((await read_guild_log_channel(message.guild.id)))  # Replace with your log channel ID
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
