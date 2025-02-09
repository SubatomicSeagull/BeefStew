import discord
import os

async def mute(interaction: discord.Interaction, member: discord.Member): 
    # cant mute yourself
    if interaction.user.id == member.id:
        await interaction.response.send_message("mute yourself? just stop talking lol", ephemeral=True)
        return
    # cant mute beefstew
    if member.id == os.getenv("CLIENTID"):
        await interaction.response.send_message("you cant silence me bitch", ephemeral=True)
        return
    # cant mute if you dont have permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    
    # if the user is in a voice channel, then server mute them 
    # this needs a rework as if a user isnt in a voice channel and gets muted they wont be server muted
    try:
        await member.edit(mute=True)
    except Exception as e:
        print("Target user is not in a voice channel, consider re-muting if they join.")
    
    # add the beefmute role if they dont have it already
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


async def unmute(interaction: discord.Interaction, member: discord.Member):
    # you cant unmute yourself
    if interaction.user.id == member.id:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    # you cant unmute beefstew
    if member.id == os.getenv("CLIENTID"):
        await interaction.response.send_message("you cant un-silence me bitch", ephemeral=True)
        return
    # cant unmute if you dont have permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return        
    
    try:
        # if the user is in a voice channel, then server unmute them 
        # this needs a rework as if a user isnt in a voice channel and gets muted they wont be server umuted
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

async def create_mute_role(guild: discord.Guild):
    try:
        print("Creating Mute Role: Defining the permissions...")
        # define each and every permission for the role - there must be a better way of doing this
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
        # move the role to the highest position it can go stopping before overriding owner
        print(f"Creating Mute Role: elevating the role to position {(len(mute_role.guild.roles)-3)}")
        await mute_role.edit(position=(len(mute_role.guild.roles)-3))
        
        
        # overwriting the permissions of the role, again there has to be better way
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
        
        # for each channel, set the role overrides, for real there HAS to be a better way
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
    # retrive the guild
    guild = member.guild
    # check to see if the mute role is registered in the server
    mute_role = discord.utils.get(guild.roles, name="BeefMute")
    if mute_role is None:
        print("Mute: no mute role, creating one")
        await create_mute_role(guild=guild)
        mute_role = discord.utils.get(guild.roles, name="BeefMute")
    try:
        # add the role to the user
        print("Mute: adding role to user")
        await member.add_roles(mute_role)
    
    except discord.Forbidden as e:
        await interaction.channel.send(f"couldnt mute {member.name} because i dont have permission {e} :(", ephemeral=True)
        
async def remove_mute_role(interaction: discord.Interaction, member: discord.Member):
    # retrive the guild
    guild = member.guild
    # check to see if the mute role is registered in the server
    mute_role = discord.utils.get(guild.roles, name="BeefMute")
    if mute_role is None:
        await create_mute_role(guild=guild)
        mute_role = discord.utils.get(guild.roles, name="BeefMute")
    try:
        # remove the role from the user
      await member.remove_roles(mute_role)
    except discord.Forbidden as e:
        await interaction.channel.send(f"couldnt unmute {member.name} because i dont have permission {e} :(", ephemeral=True)
        return
    
    except Exception as e:
        await interaction.channel.send(f"couldnt unmute {member.name} because {e}")
        return