import socket
import time
import json

class ServerInfo:
    def __init__(self, name, host_ports):
        self.name = name
        self.host_ports = host_ports

#gets the server info from the server_info.json file
def read_server_info(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        
        names = data['Name']
        host_ports = data['HostPorts']
        
        server_info_list = []
        
        for i in range(len(names)):
            name = names[i]
            ports = [port.split(':')[0] for port in host_ports[i]]
            server_info_list.append(ServerInfo(name, ports))
        
        return server_info_list

# Usage
server_info_list = read_server_info('server_info/server_info.json')
for server_info in server_info_list:
    print(f"Name: {server_info.name}, Ports: {server_info.host_ports}")


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
def host_ping(host, port, timeout, retries):
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

def pingall():
    #change so that it counts the number of ips to ping
    ipcount = 7
    #change so that it is an average of all the response times, if a response time is 0 assume the server did not respond
    response_time = 12
    response_message = (f"Pinged CCServer with {ipcount} results:\n")
    
    #repalce with a loop for each ip in the list ping it and return its average response time
    #then append a message to the response ( "{Name} is {online/offline}")
    response_message = response_message + "- ✅ CCServer is Online\n"
    response_message = response_message + "- ✅ BeefStew is Online\n"
    response_message = response_message + "- ✅ SFTP is Online (files.cosycraft.uk)\n"
    response_message = response_message + "- ✅ Origins-1.20.2 is Online (origins.cosycraft.uk)\n"
    response_message = response_message + "- ❌ Origins_Experimental is Offline (experimental.cosycraft.uk)\n"
    response_message = response_message + "- ❌ Vanilla-1.21 is Offline (vanilla.cosycraft.uk)\n"
    response_message = response_message + "- ✅ MustardVirus is Online (virus.cosycraft.uk)\n"
    
    #average all the response times
    response_message = response_message + (f"Average response time: {response_time}ms.")
    return response_message