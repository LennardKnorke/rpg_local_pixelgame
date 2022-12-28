import pygame
from config_func import *
from local_game import *
from menu import *
from multiprocessing import Process
import server
#Game Loop
    #Update window
    #Read input
    #send to server
        #Server Magic
    #Receive from server

#   -   Start
#Load window and pygame features
    #   -   Menu
    #Play
        #Decide between adventure and vs mode
            #decide to join or host
                    #Run server
                #Join as Client
                #Start Game Loop
                #at the end of the game loop exit all servers and based on command return to menu or exit

    

if __name__ == '__main__':
    #get ip-4 of mashine and prepare 2 sockets to reserver a portnumber for client and server sockets
    #Use one as a client socket to connect to a host
    HOST_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    LOKAL_IP = find_local_host()
    HOST_IP = LOKAL_IP
    searching_ports = [True, True]
    print("Pc Ip: ", LOKAL_IP)
    while searching_ports[0] == True or searching_ports[1] == True:
        if searching_ports[0] == True:#search port for client
            try:
                CLIENT_SOCKET.bind((LOKAL_IP, 0))
                CLIENT_PORT = CLIENT_SOCKET.getsockname()[1]
                print("Client_port: ", CLIENT_PORT)
                searching_ports[0] = False
            except:
                pass
        if searching_ports[1] == True:#search port for client
            try:
                HOST_SOCKET.bind((LOKAL_IP, 0))
                HOST_PORT = HOST_SOCKET.getsockname()[1]
                print("As needed server port: ", HOST_PORT)
                searching_ports[1] = False
            except:
                pass
    server_process = Process(target = server.server_main, args = (HOST_IP, HOST_PORT, HOST_SOCKET))
    #Falls raus und wieder reingegangen wird soll die original host ip gesaved bleiben
    host_ip_cpy = HOST_IP
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
                HOST_IP = main_arguments[2]
                HOST_PORT = main_arguments[3]

            Game = adventure(window = WINDOW, 
            window_size = SCREEN_SIZE, 
            window_ratios = SCREEN_RATIOS, clock = CLOCK, font_render = GAME_FONT, c_socket = CLIENT_SOCKET,c_ip = LOKAL_IP, c_port = CLIENT_PORT, host_ip = HOST_IP, host_port = HOST_PORT)
            Game.connect_client()
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
    
