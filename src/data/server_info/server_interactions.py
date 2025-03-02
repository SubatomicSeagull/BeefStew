import paramiko
import os
from data import postgres
from beefutilities.IO import file_io

async def retrive_containers_json():
   # retrive the server credentials
    try:
        host=os.getenv("SERVERIP")
        port=os.getenv("SFTPPORT")
        user=os.getenv("SFTPUSERNAME")
    except Exception as e:
        pass
    
    try:
        # start up the ssh client with a key policy, no password
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # construct the filepath to the ssh key
        ssh_key_path = file_io.construct_root_path(".ssh/id_ecdsa")
    
        # add the ssh key to the ssh client
        sshkey = paramiko.ECDSAKey.from_private_key_file(ssh_key_path)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # authenticate into the server using the key
        ssh_client.connect(hostname=host, port=port, username=user, pkey=sshkey)
        sftp = ssh_client.open_sftp()
        
        # retrive the remote containers.json
        sftp.get(os.getenv("SFTPREMOTEDIR"), (file_io.construct_data_path("server_info/containers.json")))
        
        #close the ssh connection
        sftp.close()
        ssh_client.close()
        
    except Exception as e:
        postgres.log_error(e)
        # make sure the connectoin is closed even in the event of an error
        sftp.close()
        ssh_client.close()
   
async def retreive_server_info_json():
    raise NotImplementedError


