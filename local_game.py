import pygame
import os
from config_func import *
import pickle
import time

#now its gets funny
#each lokal client does not need process information LOKALLY about enemy ai and stuff
#The lokal client only receives a list from the server with 
    #all the sprites
    #the layout of the level
    #conditions to fullfill level
    #starting location


class visual_sprite(pygame.sprite.Sprite):
    def __init__ (self, type, ratio, screen_size, player_numb = -1):
        pygame.sprite.Sprite.__init__(self)
        if type == 0:
            self.image = pygame.image.load("sprites/char/base_01.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect.center = (screen_size[0] / 2, screen_size[1] / 2)


#Class is easier manage
#Local adventure application
class adventure():
    def __init__(self, window, window_size, window_ratios, clock, font_render, c_socket, c_ip, c_port, host_ip, host_port):
        #Save online features
        self.client_socket = c_socket
        self.client_ip = c_ip
        self.c_port = c_port
        self.host_target_ip = host_ip
        self.host_target_port = host_port
        self.connected = False#needs to be true in order to run and keeps track of connection with host
        
        #Pygame features
        self.font_render = font_render
        self.screen_ratios = window_ratios
        self.screen = window
        self.screen_size = window_size
        self.clock = clock
        self.mouse_pos = pygame.mouse.get_pos()
        #Game_states
        self.player_num = 0
        self.quit = False
        #Sprites loading
        #Prepare in game features for all levels
        self.playersprite = visual_sprite(type=0, ratio = self.screen_ratios, screen_size=self.screen_size)#Load character, based on user number
        self.level_sprites = pygame.sprite.Group()#Will contain all sprites relevant for the current level
        self.load_background = pygame.transform.scale(pygame.image.load("sprites/loading.png"), (self.screen_size[0], self.screen_size[1]))
        self.load_background_rect = self.load_background.get_rect()
        #State of user input
        self.mouse_pressed = False
        self.w_jump = False
        self.a_left = False
        self.d_right = False
        self.space_defend = False
        self.shift_special = False
        self.f_healing = False

    #Receive feedback from server about the level as an intro
    def connect_client (self):
        print("Attempting to connect client")
        connection_attempts = 5
        timer = time.time()
        while connection_attempts > 0 and self.connected == False:
            self.clock.tick(30)
            self.screen.blit(self.load_background, self.load_background_rect)
            if ((time.time() - timer) >= 10):
                try:
                    self.client_socket.connect((self.host_target_ip, self.host_target_port))
                    self.connected = True
                    try:
                        self.client_socket.sendall(b"First message arrived :)")
                        data = self.client_socket.recv(1024)
                        print(data)
                    except:
                        print("Connected, but data exchange failed")
                        self.connected = False
                        connection_attempts = 0
                except:
                    pass
                connection_attempts -= 1
                if self.connected == False:
                    if connection_attempts > 0:
                        print(f"Connecting Failed. {connection_attempts} attempts left. Trying again in a few seconds")
                    else:
                        print("Failed to connect")
                    connection_attempts -= 1
                timer = time.time()
            pygame.display.update()

    def send_info(self, data):
        try:
            self.client_socket.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except:
            print(socket.error)
    def convert_input(self):
        input_list = [self.mouse_pos, self.mouse_pressed, self.w_jump, self.a_left, self.d_right, self.shift_special, self.space_defend, self.f_healing]
        r = len(input_list)
        data = ''
        for idx in range(r):
            if idx == 0:
                data += input_list[idx][0]
                data += ','
                data += input_list[idx][1]
            elif idx == r - 1:
                if input_list[idx]:
                    data += 't'
                else:
                    data += 'f'
            else:
                if input_list[idx]:
                    data += 't'
                else:
                    data += 'f'
                data += ','
        return data
    #empties the sprite list of the current level and load in the new one
    def import_sprites(self, sprites):
        self.level_sprites.empty()
        self.level_sprites.add(sprites)
    
    def run(self):
        self.running = True
        #self.import_sprites((self.playersprite))#CHANGE!
        #Lokally. refresh picture.
        #Send information about input to server
        #Receive info from server
        #Start new iteration updating visual output based on server feedback
        input_to_send = ""
        while self.running:
            self.clock.tick(30)
            #DRAW
            self.level_sprites.draw(self.screen)
            #Get input
            self.mouse_pos = pygame.mouse.get_pos()
            for input in pygame.event.get():
                if input.type == pygame.QUIT:
                    self.level = -1
                    self.running == False
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
            input_to_send = self.convert_input()
            #print(input_list)
            #Server magic missing here!
            pygame.display.update()
        #Update at the end to either go back to menu (0) end programm (-1) or anythin above to play the next level
        #if you came until here, the game wasnt cancelled and instead the next level is supposed to be loaded
        self.level +=1
        return self.level
    LEVEL = 0
