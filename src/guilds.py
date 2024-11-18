from json_handling import load_element, save_element, update_element
from data import postgres as db

def check_guild(guild):
    existing_guild = db.read(f"SELECT * FROM guilds WHERE guild_id = {guild}")
    if existing_guild is not None:
        return True
    else:
        return False

def add_guild(guild):
    try:
        db.write(f"INSERT INTO guilds (guild_id) VALUES ({guild})")
        return True
    except Exception as e:
        print(e)
        db.log_error(e)
        return False

def read_guild_log_channel(guild):
    return db.read(f"SELECT log_channel_id FROM guilds WHERE guild_id = {guild}")

def read_guild_info_channel(guild):
    return db.read(f"SELECT info_channel_id FROM guilds WHERE guild_id = {guild}")

def update_guild_log_channel(guild, channel_id):
    try:
        db.write(f"UPDATE guilds SET log_channel_id = {channel_id} WHERE guild_id = {guild}")
        return True
    except Exception as e:
        print(e)
        db.log_error(e)
        return False
    
def update_guild_info_channel(guild, channel_id):
    try:
        db.write(f"UPDATE guilds SET info_channel_id = {channel_id} WHERE guild_id = {guild}")
        return True
    except Exception as e:
        print(e)
        db.log_error(e)
        return False
    
