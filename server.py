import json
import socket
from _thread import *
import sys




#search for the local ip adress. Recommend but leave it open to change in server!
def find_local_host():
    local_mashine_name = socket.gethostname()
    local_mashine_adress = socket.gethostbyname(local_mashine_name)
    return (local_mashine_adress)

class Lokal_Server:
    def __init__(self, ip, port, serv_sock):
        self.MAX_PLAYERS = 4
        self.server_ip = ip
        self.server_port = port
        self.server_socket = serv_sock
        self.server_socket.listen(self.MAX_PLAYERS)
        self.level = 0#start with tutorial and keep increasing until the host disconnected
        #Marks which players connected and updates them
        self.current_clients = 0
        self.player_slots = [(0,False), (1,False), (2, False), (3,False)]
    def threaded_client(self, connection, player_num  = "HI"):
        connection.sendall(str.encode("Connected"))
        reply = str(player_num)
        while True:
            try:
                incoming = connection.recv(2048)
                reply = incoming.decode("utf-8")

                if not incoming:
                    print("Disconnected")
                    break
                else:
                    print("Something is working")
                connection.sendall(str.encode(reply))
            except:
                break 
    
    def run(self):
        print("Waiting for connections")
        while True:
            new_con, con_adress = self.server_socket.accept()
            print("New connection: ", con_adress)
            start_new_thread(self.threaded_client,(new_con,))



#Functions called in the main script as part of a new process.  Creates on a given socket the server.
def server_main(ip, port, assigned_socket):
    serv = Lokal_Server(ip = ip, port = port, serv_sock = assigned_socket)
    serv.run()
    print("server run out")