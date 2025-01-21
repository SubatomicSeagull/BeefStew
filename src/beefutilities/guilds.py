from data import postgres as db
import discord

async def guild_exists(guild: int):
    existing_guild = await db.read("SELECT * FROM guilds WHERE guild_id = %s", (guild,))
    if existing_guild:
        return True
    else:
        return False

async def add_guild(guild):
    try:
        await db.write("INSERT INTO guilds (guild_id) VALUES (%s)", (guild,))
        return True
    except Exception as e:
        print(e)
        await db.log_error(e)
        return False

async def read_guild_log_channel(guild: int):
    guild = await db.read("SELECT log_channel_id FROM guilds WHERE guild_id = %s", (guild,))
    return guild[0][0]

async def read_guild_info_channel(guild: int):
    guild = await db.read("SELECT info_channel_id FROM guilds WHERE guild_id = %s", (guild,))
    return guild[0][0]

async def update_guild_log_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET log_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        print(e)
        await db.log_error(e)
        return False
    
async def update_guild_info_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET info_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        print(e)
        await db.log_error(e)
        return False
    
async def update_guild_quote_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET quote_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        print(e)
        await db.log_error(e)
        return False

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
    
async def set_quotes(interaction: discord.Interaction):    
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return
    
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return
    if not await guild_exists(interaction.guild.id): 
        await add_guild(interaction.guild.id)
    await update_guild_quote_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new quotes channel.", ephemeral=True)