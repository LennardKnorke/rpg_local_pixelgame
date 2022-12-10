import pygame, os, json, ctypes
from config_func import read_options, write_options
from server import *
from game_classes import *
#Game Loop
    #Update window
    #Read input
    #send to server
        #Server Magic
    #Receive from server

#   -   Start
#Load settings and configs
#find account or create new one
    #   -   Menu
    #Play
        #Create
            #decide local ID and port
            #Run server
            #Join as Client
            #Start Game Loop
        #Join
            #Enter ip and port
            #Start Client
            #Start Game Loop
    #Options
        #Account
            #Pick account
            #New Account
        #Resolution
            #?
        #Control
    #Exit
file_list = list(os.listdir())
if "options.json" in file_list:
    local_config = read_options()
else:
    local_config = write_options()
SCREEN_HEIGHT = local_config["Screen_Height"]
SCREEN_WIDTH = local_config["Screen_Width"]
FPS = local_config["FPS"]
pygame.init()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



RUNNING = True
while RUNNING:
    next = Menu()


        
    pygame.display.update()

pygame.quit()
