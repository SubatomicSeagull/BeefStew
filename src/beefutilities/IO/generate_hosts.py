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
        print(data)
        # add smb file share entry
        container_list.append({
            "name": "<:smb:1442510224345796619>  Files",
            "ports": 445
        })
        
        for container in data:
            name = container.get("Names")
            ports = container.get("Ports")
            if ports and name != "portainer":
                if name[:3] != "int":
                    container_list.append({
                        "name": (get_container_type(name) + "  " + beautify_name(name)),
                        "ports": get_first_port(ports)
                    })
    container_list.sort(key=lambda x: x['name'].lower())
    print(container_list)
    return container_list
            
    
def beautify_name(name):
    #remove the type marker
    name = name[4:]
    
    # replace underscores and hyphens with spaces
    name = name.replace("_", " ").replace("-", " ")
    
    # capitalise each word
    name = " ".join(word.capitalize() for word in name.split())
    
    return name


def get_container_type(name):

    # separate the type marker
    type = name[:3]
    match type:
        case "mcs":
            return "<:mc:1442510206490906688>"
        case "gme":
            return "<:game:1442510198022606979>"
        case "web":
            "<:website:1442510846000496753>"
        case "int":
            return None
        case "smb":
            return "<:smb:1442510224345796619>"
        case "srv":
            return "<:service:1442510214707417258>"
        case "dnd":
            return "<:foundry:1442510184059764776>"
        case "vid":
            return "<:video:1442510835015483402>"
    return "<:service:1442510214707417258>"


# mcs	- Minecraft server 	- dirt block logo
# gme	- generic game server	- controller icon
# web	- website 		- globe icon
# int	- internal service	- none, will not display
# smb	- file share		- files icon
# srv	- generic service	- cog icon
# vid	- PVR service		- tv icon
# dnd	- dnd server		- d20 icon

def get_first_port(ports_str):
    if not ports_str:
        return None

    match = re.search(r':(\d+)->\d+/tcp\b', ports_str)
    if match:
        return int(match.group(1))

    return None
