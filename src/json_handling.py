import json
import os
from collections import OrderedDict
from server_info import server_interactions

ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), 'assets')

def load_element(file_name, element):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element not in data:
        return None
    return data[element]

def save_element(file_name, element, value):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[element] = value
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def delete_element(file_name, element):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element in data:
        del data[element]
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False

def update_element(file_name, element, value):
    file_path = os.path.join(ASSETS_FOLDER, file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    keys = element.split('.')
    d = data
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    
    d[keys[-1]] = value
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    return True

def containers_json_reformat():

    with open("src\server_info\containers.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)
        
    reformat = {}
    for i, container in enumerate(data["Name"]):
        reformat[container] = data["HostPorts"][i]
        
    cleaned_ports_list = containers_json_remove_RCON_port(reformat)
    simplified_ports_list = containers_json_simplify(cleaned_ports_list)
    
    #add sftp port
    final_data = containers_json_insert_port(simplified_ports_list, "SFTP", 22)
    
    with open("src\server_info\containers_fixed.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4) 
    
def containers_json_simplify(data):
    simplified = {}
    
    for key, ports in data.items():
        if ports:
            first = next(iter(ports.keys()))
            simplified[key] = first
    return simplified
    
def containers_json_remove_RCON_port(data):
    
    cleaned_data = {}
    
    for key, ports, in data.items():
        all_ports = []
        for port in ports:
            port_number = int(port.split("/")[0])
            all_ports.append(port_number)
        
        tcpIP_ports = []
        for port in all_ports:
            if all_ports.count(port) > 1:
              tcpIP_ports.append(port)
              
        cleaned_ports = {}
        for port in ports:
            port_number = int(port.split("/")[0])
            if port_number in tcpIP_ports:
                cleaned_ports[port_number] = ports[port]
        
        cleaned_data[key] = cleaned_ports
    return cleaned_data

def containers_json_insert_port(data, name, port):
    updated_data = OrderedDict({name: port})
    updated_data.update(data)
    return updated_data

# containers_json_reformat()