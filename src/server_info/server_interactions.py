import paramiko
import os
#from data import postgres

def retrive_containers_json():
    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Get the directory of the current script
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one folder
        project_root = os.path.dirname(current_script_dir)

# Build the path to the .ssh/id_ecdsa file
        ssh_key_path = os.path.join(project_root, ".ssh", "id_ecdsa")

        sshkey = paramiko.ECDSAKey.from_private_key_file(ssh_key_path)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(hostname=os.getenv("DBHOST"), port=os.getenv("SFTPPORT"), username=os.getenv("SFTPUSERNAME"), pkey=sshkey)
        sftp = ssh_client.open_sftp()
        
        sftp.get(os.getenv("SFTPREMOTEDIR"), (os.path.join(project_root, "server_info", "containers.json")))
        
        sftp.close()
        ssh_client.close()          

    except Exception as e:
        #postgres.log_error(e)
        print(e)
        
def retreive_server_info_json():
    raise NotImplementedError
