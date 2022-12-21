import json
import socket
from _thread import *
import sys


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
        self.input_user_template = [[0,0], False, False,False,False,False,False,False]
    def threaded_client(self, connection, player_num):
        connection.sendall(str.encode(player_num))
        reply = str(player_num)
        user_input = self.input_user_template
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
        lowest_play_idx = 0
        while True:
            new_con, con_adress = self.server_socket.accept()
            start_new_thread(self.threaded_client,(new_con, lowest_play_idx))



#Functions called in the main script as part of a new process.  Creates on a given socket the server.
def server_main(ip, port, assigned_socket):
    serv = Lokal_Server(ip = ip, port = port, serv_sock = assigned_socket)
    serv.run()


