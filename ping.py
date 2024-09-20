import socket
import time
import os

def geturls():
    raise NotImplementedError

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
    responsemessage = ""
    sum = 0
    average = 0

    #pings the host n amount of times and adds the response time to the sum
    for i in range(retries):
        t0 = time.time()
        if check(host, port, timeout):
            responsetime = ((time.time() - t0) * 1000)
            #print(str(responsetime) + " ms")
            sum = sum + responsetime
        #if the host did not respond, set sum to 0 and break the loop
        else:
            sum = 0
            retries = 0
            break
    #if the response time was not set to 0 in the unresponsive case, generate response message
    if sum != 0:
        average = sum / retries
        responsemessage = "Host " + str(host) + " responded in " + str(average)[:5] + "ms."
    else:
        responsemessage = "Host " + str(host) + " did not respond."
    
    return responsemessage