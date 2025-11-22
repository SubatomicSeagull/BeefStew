import json
import re
from data.server_info.server_interactions import retrieve_containers_json

async def containers_json_reformat():
    # define he reformat list and construct the name:port enumeration
    container_list = []
    
    try:
        data = await retrieve_containers_json()
    except Exception as e:
        data = None
        
    if data:
        data = data.decode('utf-8')
        data = json.loads(data)
        
        # add smb file share entry
        container_list.append({
            "name": "Files",
            "ports": 445
        })
        
        for container in data:
            name = container.get("Names")
            ports = container.get("Ports")
            if ports and name != "portainer":
                if name == "nginx-proxy":
                    container_list.append({
                        "name": "WWW Gateway",
                        "ports" : get_first_port(ports)
                    })
                else:
                    container_list.append({
                        "name": beautify_name(name),
                        "ports": get_first_port(ports)
                    })
    return container_list
            
    
def beautify_name(name):
    # replace underscores and hyphens with spaces
    name = name.replace("_", " ").replace("-", " ")
    
    # capitalise each word
    name = " ".join(word.capitalize() for word in name.split())
    
    return name

def get_first_port(ports_str):
    if not ports_str:
        return None

    # match something like 0.0.0.0:8123->8123/tcp or just 20000/udp
    match = re.search(r':(\d+)(?:->\d+)?', ports_str)
    if match:
        return int(match.group(1))
    
    match = re.search(r'(\d+)/\w+', ports_str)
    if match:
        return int(match.group(1))
    return None