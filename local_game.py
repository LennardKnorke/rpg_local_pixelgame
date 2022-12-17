import pygame
import os
import json
from config_func import *
from multiprocessing import Process
import server

#now its gets funny
#each lokal client does not need process information LOKALLY about enemy ai and stuff
#The lokal client only receives a list from the server with 
    #all the sprites
    #the layout of the level
    #conditions to fullfill level
    #starting location


class visual_sprite(pygame.sprite.Sprite):
    def __init__ (self, type, ratio, SCREEN_SIZE, player_numb = -1):
        pygame.sprite.Sprite.__init__(self)
        if type == 0:
            self.image = pygame.image.load("sprites/char/base_01.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)




def level_generator():
    pass
#Class is easier manage
#Local adventure application
class adventure():
    def __init__(self, hosting, ip, port, SCREEN, SCREEN_SIZE, clock, font_render, Player_number):
        #Keep the screen, fontrenderer, ip stuff saved
        self.host = hosting
        self.ip = ip,
        self.port = port
        self.player_number = Player_number
        self.font_render = font_render
        self.screen_ratio = SCREEN_SIZE[0] / 1920
        self.SCREEN = SCREEN
        self.clock = clock
        self.screen_moves = 0.25
        self.mouse_pos = pygame.mouse.get_pos()
        #Start server here?
        #Start a seperate process for the server. 
        #The server handles multiples threats for each client
        if self.host:
            Server_Process = Process(target = self.Start_server, group=None)
            Server_Process.run()
        self.start_client()

        #Prepare in game features for all levels
        self.playersprite = visual_sprite(type=0, ratio = self.screen_ratio, SCREEN_SIZE=SCREEN_SIZE)#Load character, based on user number
        self.level_sprites = pygame.sprite.Group()#Will contain all sprites relevant for the current level
        #State of user input
        self.mouse_pressed = False
        self.w_jump = False
        self.a_left = False
        self.d_right = False
        self.space_defend = False
        self.shift_special = False
        self.f_healing = False
        self.level = 0
        #Keep running until the the return is not another level
        while True:
            self.level = self.RUN()
            if self.level == -1 or self.level == 0:
                break
        
        
    def Start_server(self):
        self.server = server.Lokal_Server(self.ip, self.port)
    def start_client (self):
        pass
    #empties the sprite list of the current level and load in the new one
    def import_sprites(self, sprites):
        self.level_sprites.empty()
        self.level_sprites.add(sprites)
    
    def RUN(self):
        self.Running = True
        self.import_sprites((self.playersprite))#CHANGE!
        #Lokally. refresh picture.
        #Send information about input to server
        #Receive info from server
        #Start new iteration updating visual output based on server feedback
        input_list = []
        while self.Running:
            self.clock.tick(30)
            #DRAW
            self.level_sprites.draw(self.SCREEN)
            #Get input
            self.mouse_pos = pygame.mouse.get_pos()
            for input in pygame.event.get():
                if input.type == pygame.QUIT:
                    self.level = -1
                    self.Running == False
                elif input.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed = True
                elif input.type == pygame.KEYDOWN:
                    if input.key == pygame.K_w:
                        self.w_jump = True
                    elif input.key == pygame.K_a:
                        self.a_left = True
                    elif input.key == pygame.K_d:
                        self.d_right = True
                    elif input.key == pygame.K_SPACE:
                        self.space_defend = True
                    elif input.key == pygame.K_LSHIFT:
                        self.shift_special = True
                    elif input.key == pygame.K_f:
                        self.f_healing = True
                elif input.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pressed = False
                elif input.type == pygame.KEYUP:
                    if input.key == pygame.K_w:
                        self.w_jump = False
                    elif input.key == pygame.K_a:
                        self.a_left = False
                    elif input.key == pygame.K_d:
                        self.d_right = False
                    elif input.key == pygame.K_SPACE:
                        self.space_defend = False
                    elif input.key == pygame.K_LSHIFT:
                        self.shift_special = False
                    elif input.key == pygame.K_f:
                        self.f_healing = False
            input_list = [self.mouse_pos, self.mouse_pressed, self.w_jump, self.a_left, self.d_right, self.shift_special, self.space_defend, self.f_healing]
            print(input_list)
            #Server magic missing here!
            pygame.display.update()
        #Update at the end to either go back to menu (0) end programm (-1) or anythin above to play the next level
        #if you came until here, the game wasnt cancelled and instead the next level is supposed to be loaded
        self.level +=1
        return self.level
    LEVEL = 0
