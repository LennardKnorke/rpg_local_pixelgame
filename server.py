import json
import socket
from _thread import *
#The server runs on a different processor. 
#The main run() function of the class will start the tutorial in a different thread, and wait for incoming calls from other players
#For each player another thread is created in which information is received and send to each client
#


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
        self.player_slots = [False, False, False, False]
        #Default sheet (mouse x coordinate, mouse y coordinate), mouse pressed, move left, move right, jump....
        self.input_user_template = [[0,0], False, False,False,False,False,False,False]
        self.user_inputs = []
        #Save an input for each POSSIBLE player
        for i in range(4):
            self.user_inputs.append(self.input_user_template)
    def serv_game_thread (self):
        self.level = 0
        while self.player_slots[0]:
            if self.player_slots[3]:
                print(self.user_inputs[0], self.user_inputs[1], self.user_inputs[2], self.user_inputs[3])
            elif self.player_slots[2]:
                print(self.user_inputs[0], self.user_inputs[1], self.user_inputs[2])
            elif self.player_slots[1]:
                print(self.user_inputs[0], self.user_inputs[1])
            elif self.player_slots[0]:
                print(self.user_inputs[0])
            else:
                pass
    def threaded_client(self, connection, player_num):
        connection.sendall(str.encode(str(player_num)))
        reply = 'encoded file to send'
        while True:
            try:
                #Receive player input
                incoming = connection.recv(2048)
                #Update player_input in server
                incoming_data = incoming.decode("utf-8")
                incoming_data = incoming_data.split(',')
                self.user_inputs[player_num][0] = str(incoming_data[0])
                self.user_inputs[player_num][1] = str(incoming_data[1])
                self.user_inputs[player_num][2] = True if incoming_data[2] == 't' else False
                self.user_inputs[player_num][3] = True if incoming_data[3] == 't' else False
                self.user_inputs[player_num][4] = True if incoming_data[4] == 't' else False
                self.user_inputs[player_num][5] = True if incoming_data[5] == 't' else False
                self.user_inputs[player_num][6] = True if incoming_data[6] == 't' else False
                self.user_inputs[player_num][7] = True if incoming_data[7] == 't' else False
                #Send back stuff
                connection.sendall(str.encode(reply))
            except:
                break 
        self.player_slots[player_num] = False
    #Here: Run the level thread! then start waiting for connections and as soon as player 0 joins, start the level threat
    def run(self):
        print("Waiting for connections")
        next_player_idx = 0
        host_joined = False
        while True:
            new_con, con_adress = self.server_socket.accept()
            #update which players joined and which slot to assign next
            if self.player_slots[0] == False:
                next_player_idx = 0
                self.player_slots[0] = True
            elif self.player_slots[1] == False:
                next_player_idx = 1
                self.player_slots[1] = True
            elif self.player_slots[2] == False:
                next_player_idx = 2
                self.player_slots[2] = True
            elif self.player_slots[3] == False:
                next_player_idx = 3
                self.player_slots[3] = True
            #Checks if the host has joined and starts game thread
            if next_player_idx == 0 and host_joined == False:
                host_joined = True
                start_new_thread(self.serv_game_thread,())
            #Start client threat
            start_new_thread(self.threaded_client,(new_con, next_player_idx))





#Functions called in the main script as part of a new process.  Creates on a given socket the server.
def server_main(ip, port, assigned_socket):
    serv = Lokal_Server(ip = ip, port = port, serv_sock = assigned_socket)
    serv.run()


