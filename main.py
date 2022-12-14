import pygame, os, json, ctypes
from config_func import *
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
    #Exit
#Some Base Values, which wont change!

SCREEN_SIZE = get_monitor_specs()
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_WIDTH = SCREEN_SIZE[0]
FPS = 30
CLOCK = pygame.time.Clock()
MUSICBOX = pygame.mixer.init()

pygame.init()
pygame.font.init()
GAME_FONT = pygame.font.Font('sprites/IMMORTAL.ttf', int(32*(SCREEN_SIZE[0] / 1920)))
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mouse.set_visible(False)
RUNNING = True
while RUNNING:
    next = Menu(WINDOW, SCREEN_SIZE, CLOCK, GAME_FONT)
    #Based on Menu input changed between ending the game, running game as a client or server host
    #IF 0 End Application
    if next == 0:
        RUNNING = False
    #If 1, start adventure as host
    elif next == 1:
        pass
    #If 2, join adventure as client
    elif next == 2:
        pass
    #If 3, run Versus maps? (Big construction)
    elif next == 3:
        pass



        
    pygame.display.update()

pygame.quit()
