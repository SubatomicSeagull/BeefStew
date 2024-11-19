import socket
import time
import json
import os
from server_info.server_interactions import retrive_containers_json
from json_handling import containers_json_reformat

class ServerInfo:
    def __init__(self, name, host_ports):
        self.name = name
        self.host_ports = host_ports

# Gets the server info from the server_info.json file and returns a dictionary
def read_server_info(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        server_info_dict = {}
        
        for i, name in enumerate(data["Name"]):
            host_ports_list = data["HostPorts"][i]
            ports = [port.split('/')[0] for port in host_ports_list.keys()]
            server_info_dict[name] = ports
        
        return server_info_dict

# Usage
# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, 'server_info/server_info.json')
# server_info_dict = read_server_info(file_path)
# for name, ports in server_info_dict.items():
#     print(f"Name: {name}, Ports: {ports}")

def geturls():
    raise NotImplementedError
    
    # read ips json file formatted like:
    # url:{"Tag":"Google", "IP":"172.0.0.1", "Port":"443"}
    # which would read as [Google,172.0.0.1,443] in an array
    # host_ping() should take in tag as well for response message formatting 

#try to connect to the host through the given port
async def check(host,port,timeout):
    address = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address.settimeout(timeout)
    try:
       await address.connect((host,port))
    except:
       return False
    else:
       address.close()
       return True

#pings a given host on a given port, and averages the response time and returns a message
def ping_host(host, port, timeout, retries):
    t0 = time.time()
    response_message = ""
    sum = 0
    average = 0

    #pings the host n amount of times and adds the response time to the sum
    for i in range(retries):
        t0 = time.time()
        if check(host, port, timeout):
            response_time = ((time.time() - t0) * 1000)
            #print(str(response_time) + " ms")
            sum = sum + response_time
        #if the host did not respond, set everything to 0 and break the loop
        else:
            sum = 0
            retries = 0
            average = 0
            break
    #if the response time was not set to 0 in the unresponsive case, generate response message
    if sum != 0:
        average = sum / retries
        return average
    else:
        return 0

 # ping embed constructor
def pingembed():

    #check to see if hosts.json exists, 
    # if not, check to see if it can format containers.json,
    # if not, retrive containers.json and format it
    try:
        with open("src\server_info\hosts.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except Exception as e:     
        try:
            with open("src\server_info\containers.json", "r", encoding="utf-8-sig") as f:
                rawcontainers = json.load(f)
        except Exception as e:
            retrive_containers_json()
            
        containers_json_reformat()
            
    
    
    total_response_time = 0
    host_count = 0
    
    #embed headder
    
    #pingembed = discord.Embed(title=f"Pinged CCServer with {host_count} results:", description="", color=discord.Color.lighter_grey())
    #pingembed.set_thumbnail(url=avatarurl) # change to ccserver icon, actaully figure out how to add local files this time plz
    #pingembed.set_author(name="Beefstew", icon_url=avatarurl)
    
    for i, host, in enumerate(data):
        print(f"for {host} ping ip on port {data[host]}")
    
    #for each host in hosts.json, run ping_host()
        #start timer, ping the host
        # if its successful: 
            #stop the timer and add the time taken to ping the host truncated in ms to 2 dp to the total response time
            #generate a new string like "✅ {hostname} is Online \n" and add it to the embed body"
        # if its not successful:
            #stop the timer, dont add it to the total response time
            #generate a new string like "❌ {hostname} is Offline \n" and add it to the embed body"
        #average the response time and add it to the bottom of the embed
        #return the embed
        
pingembed()