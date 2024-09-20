import socket
import time
import os

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
    responsetime = 12
    responsemessage = (f"Pinged CCServer with {ipcount} results:\n")
    
    #repalce with a loop for each ip in the list ping it and return its average response time
    #then append a message to the response ( "{Name} is {online/offline}")
    responsemessage = responsemessage + "- ✅ CCServer is Online\n"
    responsemessage = responsemessage + "- ✅ BeefStew is Online\n"
    responsemessage = responsemessage + "- ✅ SFTP is Online (files.cosycraft.uk)\n"
    responsemessage = responsemessage + "- ✅ Origins-1.20.2 is Online (origins.cosycraft.uk)\n"
    responsemessage = responsemessage + "- ❌ Origins_Experimental is Offline (experimental.cosycraft.uk)\n"
    responsemessage = responsemessage + "- ❌ Vanilla-1.21 is Offline (vanilla.cosycraft.uk)\n"
    responsemessage = responsemessage + "- ✅ MustardVirus is Online (virus.cosycraft.uk)\n"
    
    #average all the response times
    responsemessage = responsemessage + (f"Average response time: {responsetime}ms.")
    return responsemessage