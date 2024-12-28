import paramiko
import os
#from data import postgres

def retrive_containers_json():
    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

        ssh_key_path = os.path.join(project_root, ".ssh", "id_ecdsa")
        
        sshkey = paramiko.ECDSAKey.from_private_key_file(ssh_key_path)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(hostname=os.getenv("DBHOST"), port=os.getenv("SFTPPORT"), username=os.getenv("SFTPUSERNAME"), pkey=sshkey)
        sftp = ssh_client.open_sftp()
        print("SSH authenticated...")
        sftp.get(os.getenv("SFTPREMOTEDIR"), (os.path.join(project_root, "src", "server_info", "containers.json")))
        print("Retriving containers.json...")
        sftp.close()
        ssh_client.close()          
        print("Containers.json retrieved successfully, closing SSH connection...")
    except Exception as e:
        #postgres.log_error(e)
        print(e)
        
def retreive_server_info_json():
    raise NotImplementedError
