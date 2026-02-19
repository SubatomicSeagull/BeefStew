from smb.SMBConnection import SMBConnection
import os
from datetime import datetime, timedelta

async def cleanup_downloads():
    server = os.getenv("SERVERIP")
    username = os.getenv("SMBUSER")
    password = os.getenv("SMBPASS")
    share = "Share"
    remote_dir = "/download/beefstew"
    
    print("connecting to smb server")
    smb = SMBConnection(username, password, "local_client", server, use_ntlm_v2=True, is_direct_tcp=True)
    if not smb.connect(server, 445):
        raise RuntimeError("SMB connection failed")
    print("connection successful")
    
    removed = 0
    
    for file in smb.listPath(share, remote_dir):
        if file.filename != "." and file.filename != "..":
            if datetime.fromtimestamp(file.last_write_time) < datetime.now() - timedelta(hours=1):
                print(file.filename + " is old, removing")
                smb.deleteFiles(share, remote_dir + "/" + file.filename)
                removed += 1
            else:
                print(file.filename + " is not older than an hour, skipping")
                continue
                
    print(f"> \033[95mscheduled downloads cleanup ran at {datetime.now()} removing {removed} files\033[0m")