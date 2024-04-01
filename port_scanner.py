import socket
import re
from common_ports import ports_and_services

def main():
    host = input("Enter the host name: ")
    arr = input("Enter port range without the '-': ")
    print(get_open_ports(host, list(map(int,arr.split(' '))), True))

def get_open_ports(target, port_range, verbose = False):
    flag = True
    if len(re.findall(r'[a-zA-Z]', target)) > 0: # If target contains any words obviously not IPV4 address
        try:
            socket.gethostbyname(target)
        except:
            return "Error: Invalid hostname"
    else:
            flag = False
            try:
                socket.gethostbyname(target)
            except:
                return "Error: Invalid IP address"
    open_ports = [] # Keeps a list of ports.
    port_range.sort() # Sorts the ranges from lowest to highest.
    for i in range(port_range[0], port_range[1]+1): # 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a socket connection. Is recreated to create a reset socket connection each time.
        s.settimeout(2) # Sets a socket connection timeout 5 seconds.
        if s.connect_ex((target, i)) == 0: ## checks if socket connection is succesful
            s.close()
            open_ports.append(i) # adds it to list of open ports
        else:
            s.close()
    if verbose == False:
        return(open_ports)
    else:
        if flag: # If URL
            hostname = socket.gethostbyname(target)
            res = "Open ports for {} ({})\nPORT     SERVICE".format(target, hostname)
        else: # If IP
            try:
                hostname = socket.gethostbyaddr(target)[0]
                res = "Open ports for {} ({})\nPORT     SERVICE".format(hostname, target)
            except:
                res = "Open ports for ({})\nPORT     SERVICE".format(target)
        print(open_ports)
        for i in open_ports:
            res = res + "\n{}       {}".format(i, ports_and_services[i])
        return res


main()
