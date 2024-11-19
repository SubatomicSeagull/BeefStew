import paramiko
import os

def retrive_containers_json():
    try:
        print("opening ssh client")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("connectinh to host...")
        ssh_client.connect(hostname=os.getenv("DBHOST"), port=22, username=os.getenv("SFTPUSERNAME"), password=os.getenv("SFTPPASS"))
        print("connecting sftp")
        sftp = ssh_client.open_sftp()
        
        print("retriving file")
        sftp.get(os.getenv("SFTPREMOTEDIR"), "src\\server_info\\containers.json")
        
        sftp.close()
        ssh_client.close()          
        print("ssh client closed")
    except Exception as e:
        #postgres.log_error(e)
        print(e)
        
def retreive_server_info_json():
    raise NotImplementedError