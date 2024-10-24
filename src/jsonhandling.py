import json

def guild_written(guild):
    raise NotImplementedError

def write_guild(guild):
    raise NotImplementedError

def read_log_channel(guild):
    raise NotImplementedError

def read_info_channel(guild):
    raise NotImplementedError

def write_log_channel(guild):
    raise NotImplementedError

def write_info_channel(guild):
    raise NotImplementedError

def load_responses(file_path, element):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[element]