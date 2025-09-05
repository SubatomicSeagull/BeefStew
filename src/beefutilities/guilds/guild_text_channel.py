from data import postgres as db
import discord

async def guild_exists(guild_id: int):
    existing_guild = await db.read(f"SELECT * FROM guilds WHERE guild_id = '{guild_id}';")
    if existing_guild:
        return True
    else:
        return False

async def add_guild(guild_id: int, guild_name: str):
    try:
        await db.write(f"INSERT INTO guilds (guild_id, guild_name) VALUES ({guild_id}, '{guild_name}');")
        return True
    except Exception as e:
        await db.log_error(e)
        return False

async def read_guild_log_channel(guild: int):
    guild = await db.read("SELECT log_channel_id FROM guilds WHERE guild_id = %s", (guild,))
    return guild[0][0]

async def read_guild_info_channel(guild: int):
    guild = await db.read("SELECT info_channel_id FROM guilds WHERE guild_id = %s", (guild,))
    return guild[0][0]

async def read_guild_quotes_channel(guild: int):
    guild = await db.read("SELECT quotes_channel_id FROM guilds WHERE guild_id = %s", (guild,))
    return guild[0][0]

async def update_guild_log_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET log_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        await db.log_error(e)
        return False

async def update_guild_info_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET info_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        await db.log_error(e)
        return False

async def update_guild_quote_channel(guild: int, channel_id: int):
    try:
        await db.write("UPDATE guilds SET quotes_channel_id = %s WHERE guild_id = %s", (channel_id, guild))
        return True
    except Exception as e:
        await db.log_error(e)
        return False

async def set_logs(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        # dm restriction
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return

    # cant set it if you dont have permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return

    # check to see if the server is registered in the db, add it if it isnt
    if not await guild_exists(interaction.guild.id):
        await add_guild(interaction.guild.id, interaction.guild.name)

    await update_guild_log_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new logs channel.", ephemeral=True)

async def set_info(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        # dm restriction
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return

    # cant change the info channel if you dnt have permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return

    # check to see if the server is registered in the db, add it if it isn
    if not await guild_exists(interaction.guild.id):
        await add_guild(interaction.guild.id, interaction.guild.name)

    await update_guild_info_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new info channel.", ephemeral=True)

async def set_quotes(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        # dm restriction
        await interaction.channel.send("we are literally in DMs rn bro u cant do that here...")
        return

    # cant change if you dont have perms
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("yeah yeah nice try", ephemeral=True)
        return

    # check to see if the server is registered in the db, add it if it isn
    if not await guild_exists(interaction.guild.id):
        await add_guild(interaction.guild.id, interaction.guild.name)

    await update_guild_quote_channel(interaction.guild.id, interaction.channel.id)
    await interaction.response.send_message(f"{interaction.channel.mention} is the new quotes channel.", ephemeral=True)