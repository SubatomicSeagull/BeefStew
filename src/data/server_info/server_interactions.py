import paramiko
import os
#from data import postgres

def retrive_containers_json():
    try:
        host=os.getenv("SERVERIP")
        port=os.getenv("SFTPPORT")
        user=os.getenv("SFTPUSERNAME")
    except Exception as e:
        print(e)
    
    try:

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        
        project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
        ssh_key_path = os.path.join(project_root, ".ssh", "id_ecdsa")
        print(f"Looking for SSH key in {ssh_key_path}...")
        sshkey = paramiko.ECDSAKey.from_private_key_file(ssh_key_path)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"Authenticating into {host} as {user} with key: {ssh_key_path}...")
        ssh_client.connect(hostname=host, port=port, username=user, pkey=sshkey)
        sftp = ssh_client.open_sftp()
        print("SSH authenticated...")
        sftp.get(os.getenv("SFTPREMOTEDIR"), (os.path.join(project_root, "src", "data", "server_info", "containers.json")))
        print("Retriving containers.json...")
        sftp.close()
        ssh_client.close()
        print("Containers.json retrieved successfully, closing SSH connection...")
    except Exception as e:
        #postgres.log_error(e)
        sftp.close()
        ssh_client.close()
        print(e)
        
        
def retreive_server_info_json():
    raise NotImplementedError
