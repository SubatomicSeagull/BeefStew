import socket
import time
import json
import os
from server_info.server_interactions import retrive_containers_json
from json_handling import containers_json_reformat
import discord
from datetime import datetime

#try to connect to the host through the given port
async def check(host,port,timeout):
    address = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address.settimeout(timeout)
    try:
        address.connect((host,port))
    except:
       return False
    else:
       address.close()
       return True

#pings a given host on a given port, and averages the response time and returns a message
async def ping_host(host, port, timeout, retries):
    t0 = time.time()
    sum = 0
    average = 0

    #pings the host n amount of times and adds the response time to the sum
    for i in range(retries):
        t0 = time.time()
        if await check(host, port, timeout):
            response_time = ((time.time() - t0) * 1000)
            #print(str(response_time) + " ms")
            sum = sum + response_time
        #if the host did not respond, set everything to 0 and break the loop
        else:
            sum = 0
            retries = 0
            average = 0
            break
        
    if sum != 0:
        average = sum / retries
        return average
    else:
        return 0

 # ping embed constructor
async def pingembed(interaction: discord.Interaction, icon_url, guild_name):
    
    total_response_time = 0
    host_count = len(data)
    
    #embed headder
    pingembed = discord.Embed(title=f"Pinged CCServer with {host_count} results:", description="", color=discord.Color.lighter_grey())
    pingembed.set_thumbnail(url=icon_url) # change to ccserver icon, actaully figure out how to add local files this time plz
    pingembed.set_author(name="Beefstew", icon_url=icon_url)
    
    hosts_path = os.path.join((os.path.dirname(os.path.abspath(__file__))), "server_info", "hosts.json")
    
    if not os.path.exists(hosts_path):
        generate_hosts_file()
            
    #if the hosts file is older than one day, update it
    if time.time() - os.path.getmtime(hosts_path) / 86400 > 1:
        generate_hosts_file()
    
    with open(hosts_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    
    #ping each host:port
    for i, host, in enumerate(data):
        
        host_response_time = 0
        host_response_time = await ping_host(os.getenv("SERVERIP"), data[host], 0.25, 3)    
        if host_response_time != 0:
            pingembed.add_field(name=f"✅ **{host}** is Online!", value="", inline=False)
            total_response_time = total_response_time + host_response_time
        else:
            pingembed.add_field(name=f"❌ **{host}** is Offline...", value="", inline=False)
            
    pingembed.add_field(name="", value=f"with an average response time of {round((total_response_time / host_count),2)}ms.", inline=False)
    pingembed.add_field(name="", value=f"{guild_name} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    return pingembed

def generate_hosts_file():
    retrive_containers_json()
    containers_json_reformat()
    os.remove(os.path.join((os.path.dirname(os.path.abspath(__file__))), "server_info", "containers.json"))