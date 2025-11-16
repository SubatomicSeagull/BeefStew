import paramiko
import os
from beefutilities.IO import file_io
from smb.SMBHandler import SMBHandler
import urllib

async def retrieve_containers_json():
    # retrieve the server credentials
    try:
        host=os.getenv("SERVERIP")
        port=os.getenv("SFTPPORT")
        user=os.getenv("SFTPUSERNAME")
    except Exception as e:
        pass

    # start up the ssh client with a key policy, no password
    ssh_client = paramiko.SSHClient()

    # construct the filepath to the ssh key
    ssh_key_path = file_io.construct_root_path(".ssh/id_ecdsa")

    # add the ssh key to the ssh client
    sshkey = paramiko.ECDSAKey.from_private_key_file(ssh_key_path)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # authenticate into the server using the key
    try:
        ssh_client.connect(hostname = host, port = port, username = user, pkey = sshkey, timeout = 2)
    except TimeoutError as e:
        raise TimeoutError("Connection to server timed out.")

    sftp = ssh_client.open_sftp()

    # retrieve the remote containers.json
    sftp.get(os.getenv("SFTPREMOTEDIR"), (file_io.construct_data_path("server_info/containers.json")))

    #close the ssh connection
    sftp.close()
    ssh_client.close()


# NEEDS TESTING!!!!!!!!
async def retrieve_containers_json_smb():
    
    server = os.getenv("SMBSERVER")
    username = os.getenv("SMBUSER")
    passwd = os.getenv("SMBPASS")
    remote_path = f"\\\\{server}\\{username}\\containers.json"
    opener = urllib.request.build_opener(SMBHandler)
    file_handler = opener.open(remote_path)
    data = file_handler.read()
    file_handler.close()

async def retrieve_server_info_json():
    raise NotImplementedError