import os
from smb.SMBHandler import SMBHandler
import urllib


async def retrieve_containers_json():
    
    server = os.getenv("SERVERIP")
    username = os.getenv("SMBUSER")
    passwd = os.getenv("SMBPASS")
    
    
    remote_path = f"smb://{username}:{passwd}@{server}/{username}/containers.json"
    opener = urllib.request.build_opener(SMBHandler)
    file_handler = opener.open(remote_path)
    data = file_handler.read()
    file_handler.close()
    return data

async def retrieve_server_info_json():
    raise NotImplementedError