import pygame
from config_func import *
from server import *
from local_game import *
from menu import *
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



#Getting/setting some base specs used to process the window
pygame.init()
SCREEN_SIZE = get_monitor_specs()
SCREEN_HEIGHT = SCREEN_SIZE[1]
SCREEN_WIDTH = SCREEN_SIZE[0]
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 30
CLOCK = pygame.time.Clock()
#Used to play
pygame.mixer.init()
#Used to render textq
pygame.font.init()
GAME_FONT = pygame.font.Font('sprites/IMMORTAL.ttf', int(32*(SCREEN_SIZE[0] / 1920)))

pygame.mouse.set_visible(False)
RUNNING = True
while RUNNING:
    main_arguments = Menu(WINDOW, SCREEN_SIZE, CLOCK, GAME_FONT)
    #Based on Menu input changed between ending the game, running game as a client or server host
    #IF 0 End Application
    if main_arguments[0] == 0:
        RUNNING = False
    #If 1, start adventure as host
    elif main_arguments[0] == 1:
        adventure(hosting = True, ip = main_arguments[1], port = [2], SCREEN = WINDOW, SCREEN_SIZE = SCREEN_SIZE, clock = CLOCK, font_render = GAME_FONT, Player_number = 0)
    #If 2, join adventure as client
    elif main_arguments[0] == 2:
        adventure(hosting = False, ip = main_arguments[1], port = [2], SCREEN = WINDOW, SCREEN_SIZE = SCREEN_SIZE, clock = CLOCK, font_render = GAME_FONT)

    #If 3, run Versus maps? (Big construction). Do later or do we need it?
    elif main_arguments[0] == 3:
        RUNNING = False

pygame.quit()
