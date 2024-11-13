import json

def guild_written(guild):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)    
    for key in data.keys():
        if str(key) == str(guild):   
            return True
    return False

def write_guild(guild):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)
        new_guild_entry = {
            "log_channel_id": "",
            "info_channel_id": ""
        }
        data[str(guild)] = new_guild_entry
        with open("src\\assets\\guild_config.json", "w") as file:
            json.dump(data, file, indent=4)

def read_log_channel(guild):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)
    return data[str(guild)]["log_channel_id"]

def read_info_channel(guild):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)
    return data[str(guild)]["info_channel_id"]

def write_log_channel(guild, channel_id):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)
    data[str(guild)]["log_channel_id"] = str(channel_id)
    with open("src\\assets\\guild_config.json", "w") as file:
        json.dump(data, file, indent=4)

def write_info_channel(guild, channel_id):
    with open("src\\assets\\guild_config.json", "r") as file:
        data = json.load(file)
    data[str(guild)]["info_channel_id"] = str(channel_id)
    with open("src\\assets\\guild_config.json", "w") as file:
        json.dump(data, file, indent=4)

def load_element(file_path, element):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[element]