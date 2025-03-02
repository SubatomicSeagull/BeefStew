import os
import json
from collections import OrderedDict
from data.server_info.server_interactions import retrive_containers_json
from beefutilities.IO import file_io

async def containers_json_reformat():
    # construct server info file path
    containers_path = file_io.construct_data_path("server_info/containers.json")
    hosts_path = file_io.construct_data_path("server_info/hosts.json")
    
    # open containers.json
    with open(containers_path, "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    
    # define he reformat list and construct the name:port enumeration
    reformat = {}
    for i, container in enumerate(data["Name"]):
        reformat[container] = data["HostPorts"][i]
        
    # clean up the ports lit
    cleaned_ports_list = await containers_json_remove_RCON_port(reformat)
    simplified_ports_list = await containers_json_simplify(cleaned_ports_list)
    
    #add sftp port
    final_data = await containers_json_insert_port(simplified_ports_list, "Files", (int(os.getenv("SFTPPORT"))))
    
    # write to hosts.json
    with open(hosts_path, "w", encoding="utf-8") as file:
        json.dump(final_data, file, indent=4) 
    
async def containers_json_simplify(data):
    simplified = {}
    
    # for each port, pair it with the hostname
    for key, ports in data.items():
        if ports:
            first = next(iter(ports.keys()))
            simplified[key] = first
    return simplified
    
async def containers_json_remove_RCON_port(data):
    
    cleaned_data = {}
    
    # remove the rcon port after port/rcon
    for key, ports, in data.items():
        all_ports = []
        for port in ports:
            port_number = int(port.split("/")[0])
            all_ports.append(port_number)
        
        #seperate the tcp/ip port from the rcon port
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

async def containers_json_insert_port(data, name, port):
    updated_data = OrderedDict({name: port})
    updated_data.update(data)
    return updated_data

async def generate_hosts_file():
    await retrive_containers_json()
    await containers_json_reformat()
    
    # pathfind to containers.json
    containers_path = file_io.construct_data_path("server_info/containers.json")
    
    # delete containers.json after hosts.json has been created
    os.remove(containers_path)