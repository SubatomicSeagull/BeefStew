import paramiko
import os

def retrive_containers_json():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=os.getenv("DBHOST"), port=22, username=os.getenv("SFTPUSERNAME"), password=os.getenv("SFTPPASS"))
        sftp = ssh_client.open_sftp()
        
        sftp.get(os.getenv("SFTPREMOTEDIR"), "src\\server_info\\containers.json")
        
        sftp.close()
        ssh_client.close()            
    except Exception as e:
        #postgres.log_error(e)
        print(e)
        
def retreive_server_info_json():
    raise NotImplementedError