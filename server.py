import json
import socket
from _thread import *
import sys

#search for the local ip adress. Recommend but leave it open to change in server!
def find_local_host():
    local_mashine_name = socket.gethostname()
    local_mashine_adress = socket.gethostbyname(local_mashine_name)
    return (local_mashine_name, local_mashine_adress)

def check_port(ip,port_number):
    pass

class Lokal_Server:
    def __init__(self):
        self.local_name = find_local_host()[0]
        self.local_ip = find_local_host()[1]
        self.port = 5555 #CHANGE! make it manual!
        self.adress = (self.local_ip, self.port)
        #Server subclass which will manage connection and create new client threats
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def bind_serv_to_port (self):
        try:
            self.server.bind((self.local_ip, self.port))
            self.server.listen(4)#Allow up to 4 players to join
        except socket.error:
            print(str(socket.error))
