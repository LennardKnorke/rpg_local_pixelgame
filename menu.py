import pygame
import os
import json
from config_func import *
class Menu_button(pygame.sprite.Sprite):
    def __init__(self, button_type, text, SCREEN_SIZE, index, FONT, assigned_layer):
        pygame.sprite.Sprite.__init__(self)
        self.default_button_bool = button_type#type? default: text stays, the other varies with input
        self.og_text = text#Original text off button
        self.displayed_text = self.og_text#displayed text
        self.menu_layer = assigned_layer#save menu layer
        self.index = index#save its position relative to other buttons
        self.SCREEN_SIZE = SCREEN_SIZE#could be useful
        self.Font_render = FONT#save the fontmaker
        #2 kind of buttons
            #First default. Can be clicked to navigate the menu
            #Load default picture and adjust size
        self.image = pygame.image.load("sprites/menu/default.png")
        self.image = pygame.transform.scale(self.image, (self.SCREEN_SIZE[0] / 5,self.SCREEN_SIZE[1] / 10))
        self.rect = self.image.get_rect()
        self.rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))
        self.displayed_text = FONT.render(self.displayed_text, False, (0,0,0))
        self.displayed_text_rect = self.displayed_text.get_rect()
        self.displayed_text_rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - index))
        
        #The other one gets 2 extra settings. one keeps tracking whether the input is currently changing and the input itself
        if not self.default_button_bool:
            self.changing = False
            self.input_string_cpy = ""

    def click (self):
        if self.menu_layer == 3:
            self.update_text(self.input_string_cpy)
        if self.index == 0:
            return True
        else: 
            return False
    #Given an input, updates the button text
    def update_text (self, new_text):
        self.displayed_text = self.Font_render.render(new_text, False, (0,0,0))
        self.displayed_text_rect = self.displayed_text.get_rect()
        self.displayed_text_rect.center = (self.SCREEN_SIZE[0] / 2, self.SCREEN_SIZE[1] / (3 - self.index))
    #Annoying drawing mechanic :/
    def draw_text(self, SCREEN):
        SCREEN.blit(self.displayed_text, self.displayed_text_rect)
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
    def update(self, SCREEN):
        self.draw(SCREEN)
        self.draw_text(SCREEN)
    def return_input(self):
        return (self.input_string_cpy)

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
    Layer_3 = pygame.sprite.Group()#IP + Port
    
    #Load Background
    background = pygame.image.load(f'sprites/menu/BGMenu.png')
    background = pygame.transform.scale(background, (SCREEN_SIZE[0], SCREEN_SIZE[1]))
    background_rect = background.get_rect()

    for layer in range(0,4):
        idx = 0
        for button in button_list[f'Layer_{layer}']:
            tmp_button = Menu_button(button["default"], button["text"], SCREEN_SIZE, idx, FONT = FONT, assigned_layer= layer)
            if layer == 0:
                Layer_0.add(tmp_button)
            elif layer == 1:
                Layer_1.add(tmp_button)
            elif layer == 2:
                Layer_2.add(tmp_button)
            elif layer == 3:
                Layer_3.add(tmp_button)
            idx += 1
    #Mouse
    ACTIVE_MOUSE = True
    MOUSE = Mouse_Sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], SCREEN_SIZE = SCREEN_SIZE)
    #Menu layer management
    Current_layer = 0
    Layers = [Layer_0, Layer_1, Layer_2, Layer_3]
    #Selected:
    PLAY_ADVENTURE = False
    HOST = False
    adress = ["",""]
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
                return (0, adress[0], adress[1])
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
                    elif ACTIVE_MOUSE == False and Current_layer == 3:
                        for sprite in Layers[Current_layer].sprites():
                            sprite.changing == False
                            sprite.update_text(sprite.og_text)
                            sprite.input_string_cpy = ""
                        ACTIVE_MOUSE = True    
                    #Or go back 1 page
                    else:
                        Current_layer -= 1
                #Handle enter button

                if event.key == pygame.K_RETURN:
                    if ACTIVE_MOUSE and Current_layer == 3:
                        if adress[0] != "" and adress[1] != "" and valid_ip(adress):
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
                    elif Current_layer == 3:
                        ACTIVE_MOUSE = True
                        idx = 0
                        for sprite in Layers[Current_layer].sprites():
                            adress[idx] = sprite.return_input()
                            sprite.changing = False
                            idx += 1
                elif event.key == pygame.K_BACKSPACE and Current_layer ==3 and not ACTIVE_MOUSE:
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        if sprite.changing:
                            sprite.input_string_cpy = sprite.input_string_cpy[:-1]
                elif Current_layer == 3 and not ACTIVE_MOUSE:
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        if sprite.changing:
                            sprite.input_string_cpy += event.unicode
                            sprite.update_text(sprite.input_string_cpy)       

            if event.type == pygame.MOUSEBUTTONDOWN:
                #For every sprite clicked (its only one)
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
                    #In the third layer. clicked on one of the field.
                    #Deactive mouse and enabling text input higher up
                    else:
                        if ACTIVE_MOUSE:
                            ACTIVE_MOUSE = False
                            sprite.changing = True
                        else:
                            idx = 0
                            for s in Layers[Current_layer].sprites():
                                adress[idx] = s.return_input()
                                idx += 1
                            ACTIVE_MOUSE = True
                            sprite.changing = False
        pygame.display.update()