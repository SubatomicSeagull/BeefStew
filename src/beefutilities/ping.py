import socket
import time
import json
import os
from beefutilities.IO.generate_hosts import generate_hosts_file
from beefutilities.IO import file_io
import discord
from datetime import datetime

async def check(host,port,timeout):
    # instantiate the socket and set timeout params
    address = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    address.settimeout(timeout)
    try:
        # try to connect to the host:post
        address.connect((host,port))
    except:
       return False
    else:
       # close the connection
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