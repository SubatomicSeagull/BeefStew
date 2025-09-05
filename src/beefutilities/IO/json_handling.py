import json
import os
from collections import OrderedDict
from beefutilities.IO import file_io

# global assets folder path
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

def load_element(file_name, element):
    # construct the file path
    file_path = os.path.join(ASSETS_FOLDER, file_name)

    # retrieve the given element
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element not in data:
        return None
    return data[element]

def save_element(file_name, element, value):
    #construct the file path
    file_path = os.path.join(ASSETS_FOLDER, file_name)

    # save the value to the given element if the file exists
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[element] = value

    #write the data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 4)

def delete_element(file_name, element):
    # construct the file path
    file_path = os.path.join(ASSETS_FOLDER, file_name)

    # open the json file
    with open(file_path, 'r') as file:
        data = json.load(file)
    if element in data:
        # remove the element of it exists
        del data[element]
        # write the new json file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent = 4)
        return True
    return False

def update_element(file_name, element, value):
    # construct the file path
    file_path = os.path.join(ASSETS_FOLDER, file_name)

    # open the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # split the elements and match them with the keys
    keys = element.split('.')
    d = data
    for key in keys[:-1]:
        d = d.setdefault(key, {})

    d[keys[-1]] = value

    # write the updated file.
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 4)
    return True


### uhhhh these are reused from generate hosts and i dont know which ones are used
# FIXME: plz fix
def containers_json_reformat():
    containers_path = file_io.construct_data_path("server_info/containers.json")
    hosts_path = file_io.construct_data_path("server_info/hosts.json")
    with open(containers_path, "r", encoding = "utf-8-sig") as file:
        data = json.load(file)

    reformat = {}
    for i, container in enumerate(data["Name"]):
        reformat[container] = data["HostPorts"][i]

    cleaned_ports_list = containers_json_remove_RCON_port(reformat)
    simplified_ports_list = containers_json_simplify(cleaned_ports_list)

    #add sftp port
    final_data = containers_json_insert_port(simplified_ports_list, "Files", (int(os.getenv("SFTPPORT"))))

    with open(hosts_path, "w", encoding = "utf-8") as file:
        json.dump(final_data, file, indent = 4)

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