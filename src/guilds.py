from data import postgres as db

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