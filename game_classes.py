import pygame
import os
import json
from config_func import *

class Player(pygame.sprite.Sprite):
    pass

class Menu_button(pygame.sprite.Sprite):
    def __init__(self, button_type, text, SCREEN_SIZE, index, FONT, assigned_layer, ip_adress = None):
        pygame.sprite.Sprite.__init__(self)
        self.button_type = button_type
        self.og_text = text
        self.button_text = self.og_text
        self.menu_layer = assigned_layer
        self.index = index
        self.SCREEN_SIZE = SCREEN_SIZE
        self.Font_render = FONT
        #2 kind of buttons
            #First default. Can be clicked to navigate the menu
        if self.button_type == "default":
            #Load default picture and adjust size
            self.image = pygame.image.load("sprites/menu/default.png")
            self.image = pygame.transform.scale(self.image, (self.SCREEN_SIZE[0] / 5,self.SCREEN_SIZE[1] / 10))
            self.rect = self.image.get_rect()
            self.rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))
            #Load text for a default button
            self.button_text = FONT.render(self.button_text, False, (0,0,0))
            self.button_text_rect = self.button_text.get_rect()
            self.button_text_rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))
            
            #Used to add ip and port adress
        else:
            #Load default picture and adjust size
            self.image = pygame.image.load("sprites/menu/default.png")
            self.image = pygame.transform.scale(self.image, (self.SCREEN_SIZE[0] / 5,self.SCREEN_SIZE[1] / 10))
            self.rect = self.image.get_rect()
            self.rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))
            self.active_input = False
            #Load text for a default button
            self.button_text = FONT.render(self.button_text, False, (0,0,0))
            self.button_text_rect = self.button_text.get_rect()
            self.button_text_rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))


    def click (self):
        if self.button_type == "adress":
            pass
        if self.index == 0:
            return True
        else: 
            return False
    def update_text (self, new_text):
        self.button_text = self.Font_render.render(new_text, False, (0,0,0))
        self.button_text_rect = self.button_text.get_rect()
        self.button_text_rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - self.index))

    def draw_text(self, SCREEN):
        SCREEN.blit(self.button_text, self.button_text_rect)
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
    def update(self, SCREEN):
        self.draw(SCREEN)
        self.draw_text(SCREEN)

class Mouse_Sprite(pygame.sprite.Sprite):
    def __init__(self, mousex, mousey, SCREEN_SIZE):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/menu/curs.png")
        self.image = pygame.transform.scale(self.image,(40 * (SCREEN_SIZE[0] / 1920), 40 * (SCREEN_SIZE[1] / 1080)))
        self.rect = self.image.get_rect()
        self.rect.center = (mousex, mousey)
    def moving(self, x,y):
        self.rect.center = (x,y)

        #SCREEN.blit(self.image, self.rect)
#Left to do: 
#   Instand update on IP and Port input
#   Check IP/ Port validity
def Menu(SCREEN, SCREEN_SIZE, CLOCK, FONT):
    MENU_RUNNING = True
    button_list = json.load(open("Sprites/menu/button_list.json", 'r'))
    Layer_0 = pygame.sprite.Group()#Play + End
    Layer_1 = pygame.sprite.Group()#Adventure + Versus
    Layer_2 = pygame.sprite.Group()#Host + Join
    Layer_3 = pygame.sprite.Group()#IP window
    Layer_4 = pygame.sprite.Group()#IP display
    
    #Load Background
    background = pygame.image.load(f'sprites/menu/BGMenu.png')
    background = pygame.transform.scale(background, (SCREEN_SIZE[0], SCREEN_SIZE[1]))
    background_rect = background.get_rect()

    for layer in range(0,4):
        idx = 0
        for button in button_list[f'Layer_{layer}']:
            tmp_button = Menu_button(button["type"], button["text"], SCREEN_SIZE, idx, FONT = FONT, assigned_layer= layer)
            if layer == 0:
                Layer_0.add(tmp_button)
            elif layer == 1:
                Layer_1.add(tmp_button)
            elif layer == 2:
                Layer_2.add(tmp_button)
            elif layer == 3:
                Layer_3.add(tmp_button)
            else:
                Layer_4.add(tmp_button)
            idx += 1
    #Mouse
    ACTIVE_MOUSE = True
    MOUSE = Mouse_Sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], SCREEN_SIZE=SCREEN_SIZE)
    #Menu layer management
    Current_layer = 0
    Layers = [Layer_0,Layer_1, Layer_2,Layer_3]
    #Selected:
    PLAY_ADVENTURE = False
    HOST = False
    adress = ["",""]
    adress_idx = -1
    user_input = ""
    while MENU_RUNNING:
        CLOCK.tick(30)
        SCREEN.blit(background,background_rect)
        
        Layers[Current_layer].update(SCREEN)
        if ACTIVE_MOUSE:
            SCREEN.blit(MOUSE.image, MOUSE.rect)
            mouse_pos = pygame.mouse.get_pos()
            MOUSE.moving(mouse_pos[0], mouse_pos[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:

                #######
                #DEVELOPER BUTTON. CLICK TO JUMP OVER ALL
                if event.key == pygame.K_q:
                    return (1, '192.168.2.199', '4200')
                ###DELETE PART ABOVE
                #######

                #Handles escape button
                if event.key == pygame.K_ESCAPE:
                    #If in the main page, exit application
                    if Current_layer == 0:
                        return (0, adress[0], adress[1])
                    #if currently the mouse is not activated, activate it again
                    elif ACTIVE_MOUSE == False:
                        ACTIVE_MOUSE = True    
                        user_input = ""
                    #Or go back 1 page
                    else:
                        Current_layer -= 1
                #Handle enter button
                if event.key == pygame.K_RETURN and Current_layer == 3:
                    if ACTIVE_MOUSE == False:
                        ACTIVE_MOUSE = True
                        adress[adress_idx] = user_input
                        user_input = ""
                    elif ACTIVE_MOUSE and adress[0] != "" and adress[1] != "" and valid_ip(adress):
                        
                        if PLAY_ADVENTURE:
                            if HOST:
                                return (1, adress[0], adress[1])
                            else:
                                return (2, adress[0], adress[1])
                        else:
                            if HOST:
                                return (3, adress[0], adress[1])
                            else:
                                return (4, adress[0], adress[1])

                if event.key == pygame.K_BACKSPACE and ACTIVE_MOUSE == False and Current_layer == 3:
                    user_input = user_input[:-1]
                elif ACTIVE_MOUSE == False and Current_layer == 3:
                    user_input += event.unicode
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        sprite.update_text(user_input)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                    clicked = sprite.click()
                    
                    if Current_layer == 0:
                        if clicked:#Clicked to "Play"
                            Current_layer = 1
                        else:
                            return [0]#Clicked to "exit"
                
                    elif Current_layer == 1:
                        if clicked:
                            PLAY_ADVENTURE = True#Clicked to "adventure"
                        else:
                            PLAY_ADVENTURE = False#Clicked to "pvp"
                        Current_layer = 2
                    
                    elif Current_layer == 2:
                        if clicked:
                            HOST = True#Clicked to "host"
                        else:
                            HOST = False#Clicked to "join"
                        Current_layer = 3
                    elif Current_layer == 3:
                        if clicked:#Clicked to "join"
                            ACTIVE_MOUSE = not ACTIVE_MOUSE
                            adress_idx = 0
                        else:
                            ACTIVE_MOUSE = not ACTIVE_MOUSE
                            adress_idx = 1
        pygame.display.update()

def adventure():
    pass