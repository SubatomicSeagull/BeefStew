import discord
from discord import Message, app_commands
from discord.ext import commands
import random
from json_handling import load_element
from datetime import datetime
    
async def kick_message_embed(mod: discord.Member, member: discord.Member, reason: str, icon_url, guild_name):
        kickembed = discord.Embed(title=f"Kicked!", color=discord.Color.dark_orange())
        kickembed.set_thumbnail(url=member.avatar.url)
        kickembed.add_field(name="", value=get_kick_message(member, reason), inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value=f"**Kicked by**: <@{mod.id}>", inline=False)
        kickembed.add_field(name="", value=f"**Reason**: {reason}", inline=False)    
        kickembed.add_field(name="", value="", inline=False)
        kickembed.add_field(name="", value="", inline=False) 
        kickembed.set_author(name="Beefstew", icon_url=icon_url)
        kickembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return kickembed

def get_kick_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"id": member.id})()
    responses = load_element("responses.json", "kick_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

async def ban_message_embed(mod: discord.Member, member: discord.Member, reason: str, icon_url, guild_name):
        banembed = discord.Embed(title=f"BANNED!", color=discord.Color.red())
        banembed.set_thumbnail(url=member.avatar.url)
        banembed.add_field(name="", value=get_ban_message(member, reason), inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value=f"**Banned by**: <@{mod.id}>", inline=False)
        banembed.add_field(name="", value=f"**Reason**: {reason}", inline=False)    
        banembed.add_field(name="", value="", inline=False)
        banembed.add_field(name="", value="", inline=False) 
        banembed.set_author(name="Beefstew", icon_url=icon_url)
        banembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")      
        return banembed
    
def get_ban_message(member: discord.Member, reason: str): 
    membername = type('Member', (object,), {"id": member.name})()
    responses = load_element("responses.json", "ban_messages")    
    chosen_response = random.choice(responses).format(member=membername, reason=reason)
    return chosen_response

async def create_mute_role(guild: discord.Guild):
    try:
        print("Creating Mute Role: Defining the permissions...")
        permissions = discord.Permissions()    
        permissions.update(
            kick_members=False,
            ban_members=False,
            manage_channels=False,
            manage_guild=False,
            add_reactions=True,
            view_audit_log=False,
            read_messages=True,
            send_messages=False,
            manage_messages=False,
            embed_links=False,
            attach_files=False,
            read_message_history=True,
            mention_everyone=False,
            use_external_emojis=True,
            connect=True,
            speak=False,
            mute_members=False,
            deafen_members=False,
            move_members=False,
            use_voice_activation=True,
            change_nickname=True,
            manage_nicknames=False,
            manage_roles=False,
            manage_webhooks=False,
            manage_emojis= False
        )    
        print("Creating Mute Role: creating the role")
        mute_role = await guild.create_role(name="BeefMute", permissions=permissions,)
        print(f"Creating Mute Role: elevating the role to position {(len(mute_role.guild.roles)-3)}")
        await mute_role.edit(position=(len(mute_role.guild.roles)-3))
        
        print("Creating Mute Role: creating override permissions")
        overwrite = discord.PermissionOverwrite()
        overwrite.kick_members=False
        overwrite.ban_members=False
        overwrite.manage_channels=False
        overwrite.manage_guild=False
        overwrite.add_reactions=True
        overwrite.view_audit_log=False
        overwrite.read_messages=True
        overwrite.send_messages=False
        overwrite.manage_messages=False
        overwrite.embed_links=False
        overwrite.attach_files=False
        overwrite.read_message_history=True
        overwrite.mention_everyone=False
        overwrite.use_external_emojis=True
        overwrite.connect=True
        overwrite.speak=False
        overwrite.mute_members=False
        overwrite.deafen_members=False
        overwrite.move_members=False
        overwrite.use_voice_activation=True
        overwrite.change_nickname=True
        overwrite.manage_nicknames=False
        overwrite.manage_roles=False
        overwrite.manage_webhooks=False
        overwrite.manage_emojis= False   
        
        for channel in guild.channels:
            print(f"Creating Mute Role: setting permission overrides in {channel.name}")
            try:
                await channel.set_permissions(mute_role, overwrite=overwrite)
            except discord.Forbidden:
                print(f"Failed to set permissions in {channel.name}. Missing permissions.")
            except discord.HTTPException as e:
                print(f"Failed to set permissions in {channel.name}: {e}")
                
    except discord.Forbidden:
        print("Tried to create the mute role, but no permissions")
        
async def add_mute_role(interaction: discord.Interaction, member: discord.Member):
    guild = member.guild
    mute_role = discord.utils.get(guild.roles, name="BeefMute")
    if mute_role is None:
        print("Mute: no mute role, creating one")
        await create_mute_role(guild=guild)
        mute_role = discord.utils.get(guild.roles, name="BeefMute")
    try:
        print("Mute: adding role to user")
        await member.add_roles(mute_role)
    except discord.Forbidden as e:
        await interaction.channel.send(f"couldnt mute {member.name} because i dont have permission {e} :(", ephemeral=True)
        
async def remove_mute_role(interaction: discord.Interaction, member: discord.Member):
    guild = member.guild
    mute_role = discord.utils.get(guild.roles, name="BeefMute")
    if mute_role is None:
        await create_mute_role(guild=guild)
        mute_role = discord.utils.get(guild.roles, name="BeefMute")
    try:
      await member.remove_roles(mute_role)
    except discord.Forbidden as e:
        await interaction.channel.send(f"couldnt unmute {member.name} because i dont have permission {e} :(", ephemeral=True)
        return
    except Exception as e:
        await interaction.channel.send(f"couldnt unmute {member.name} because {e}")
        return

