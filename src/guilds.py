from json_handling import load_element, save_element, update_element

def guild_written(guild):
    data = load_element("guild_config.json", str(guild))
    return data is not None

def write_guild(guild):
    new_guild_entry = {
        "log_channel_id": "",
        "info_channel_id": ""
    }
    save_element("guild_config.json", str(guild), new_guild_entry)

def read_log_channel(guild):
    data = load_element("guild_config.json", str(guild))
    return data["log_channel_id"]

def read_info_channel(guild):
    data = load_element("guild_config.json", str(guild))
    return data["info_channel_id"]

def write_log_channel(guild, channel_id):
    update_element("guild_config.json", 
                   f"{guild}.log_channel_id", str(channel_id))

def write_info_channel(guild, channel_id):
    update_element("guild_config.json", 
                   f"{guild}.info_channel_id", str(channel_id))