import pygame
from config_func import *
from local_game import *
from menu import *
from multiprocessing import Process
import server

###Structure###

#Main()
    #1.
    #Find local ip, secure ports for client and host sockets
    #Get screen details
    #Other details helpful for the application on each respective pc
    #2. 
    #Menu
    #(Profile management! implement back again)
    #Play or Exit
        #If Play:
        #Host or Join
        #If Host, exit menu and start the shit show
        #If join, enter ip and port
    #3. Game Cycle
        #If Hosting, start server process. SEPERATE PROCESS STARTS HERE!!:
            #runs server_main function from server.py
            #create a server class instance
            #wait for incoming connections
                #For each connection start a thread in which in client keeps sending and receiving
            #As soon as the first player (the host) joins, start the game loop

    #4. Game
        #Start client. connect to host
        #Game loop:
            #DRAW
            #Get Input
            #Send input to server
            #Get feedback from server
            #Repeat


if __name__ == '__main__':
    #get ip-4 of mashine and prepare 2 sockets to reserver a portnumber for client and server sockets
    #Use one as a client socket to connect to a host
    #HOST_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOKAL_IP = find_local_host()
    print("Local Ip: ", LOKAL_IP)

    CLIENT_SOCKET.bind((LOKAL_IP, 0))
    CLIENT_PORT = CLIENT_SOCKET.getsockname()[1]

    HOST_SOCKET.bind((LOKAL_IP, 0))
    HOST_PORT = HOST_SOCKET.getsockname()[1]
    print("Client_port: ", CLIENT_PORT)
    print("Host_port: ", HOST_PORT)

    server_process = Process(target = server.server_main, args = (HOST_SOCKET,True))
    #keep a copy of reserved host socket port!
    host_ip_cpy = LOKAL_IP
    host_port_cpy = HOST_PORT
    #Setting windows specks
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    SCREEN_SIZE = get_monitor_specs()
    creator_to_user_ratio_width  = SCREEN_SIZE[0] / 1920
    creator_to_user_ratio_height  = SCREEN_SIZE[1] / 1080
    SCREEN_RATIOS = (creator_to_user_ratio_width, creator_to_user_ratio_height)
    WINDOW = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
    pygame.display.set_caption("Tales of Boys being Boys")
    FPS = 30
    CLOCK = pygame.time.Clock()
    GAME_FONT = pygame.font.Font('sprites/IMMORTAL.ttf', int(32 * creator_to_user_ratio_width))
    pygame.mouse.set_visible(False)

    #Main application loop. swithces between menu and game application
    APP_RUNNING = True
    while APP_RUNNING:
        main_arguments = Menu(WINDOW, SCREEN_SIZE, SCREEN_RATIOS, CLOCK, GAME_FONT)
        #main_arguments[keeprunning?_bool, shall_I_host?_bool, host_ip(in case of joining), host port] len 4
        if main_arguments[0] == False:
            APP_RUNNING = False
        else:
            #If host, start server
            if main_arguments[1] == True:
                server_process.start()
            #otherwise save the host ip and port number
            else:
                #How to handle ip adress?
                #HOST_IP = main_arguments[2]
                HOST_PORT = main_arguments[3]

            Game = adventure(window = WINDOW, window_size = SCREEN_SIZE, window_ratios = SCREEN_RATIOS, clock = CLOCK, font_render = GAME_FONT, c_socket = CLIENT_SOCKET,c_ip = LOKAL_IP, c_port = CLIENT_PORT)
            Game.connect_client(HOST_PORT)
            if Game.connected:
                Game.run()
            #After the game aint running anymore, check if the desire was to quit?
            #Else: Fix the default ip, host
            #TO DO: Rejoining?  socket rebinding necessary?
            if Game.quit:
                APP_RUNNING = False
        if APP_RUNNING:
            HOST_IP = host_ip_cpy
            HOST_PORT = host_port_cpy
        if server_process.is_alive():
            server_process.kill()
    HOST_SOCKET.close()
    CLIENT_SOCKET.close()
    pygame.quit()
    
