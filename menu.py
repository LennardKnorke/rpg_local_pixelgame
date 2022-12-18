import pygame
import os
import json
from config_func import *

class Menu_button(pygame.sprite.Sprite):
    def __init__(self, button_type, text, screen_size, index, font, assigned_layer):
        pygame.sprite.Sprite.__init__(self)
        self.default_button_bool = button_type#type? default: text stays, the other varies with input
        self.og_text = text#Original text off button
        self.displayed_text = self.og_text#displayed text
        self.menu_layer = assigned_layer#save menu layer
        self.index = index#save its position relative to other buttons
        self.screen_size = screen_size#could be useful
        self.Font_render = font#save the fontmaker
        
        #2 kind of buttons
        #First default. Can be clicked to navigate the menu
        #second type used to save ip and port adress to connect to
            #changes while using it

        #As every pygame sprite class a button has:
            #an image: what you see
            #the image's rect: its collision box/position
            #(mask): faster to calculate collision between sprites
        self.image = pygame.image.load("sprites/menu/default.png")
        self.image = pygame.transform.scale(self.image, (self.screen_size[0] / 5,self.screen_size[1] / 10))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen_size[0] / 2, self.screen_size[1] / (3 - index))
        self.displayed_text = self.Font_render.render(self.displayed_text, False, (0,0,0))
        self.displayed_text_rect = self.displayed_text.get_rect()
        self.displayed_text_rect.center = (self.screen_size[0] / 2, self.screen_size[1] / (3 - index))
        self.mask = pygame.mask.from_surface(self.image)
        #The second button type gets one gets 2 extra settings. 
        #one keeps tracking whether the input is currently changing 
        # and the input itself
        if not self.default_button_bool:
            self.changing = False
            self.input_string_cpy = ""
    #only two buttons. therefore return true or false whether the upper or lower button was pressed
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
        self.displayed_text_rect.center = (self.screen_size[0] / 2, self.screen_size[1] / (3 - self.index))
    #Annoying drawing mechanics :/
    #Cant draw the two connected images together so two draw functions called in the update function!
    def draw_text(self, SCREEN):
        SCREEN.blit(self.displayed_text, self.displayed_text_rect)
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
    def update(self, SCREEN):
        self.draw(SCREEN)
        self.draw_text(SCREEN)
    def return_input(self):
        return (self.input_string_cpy)
#Cursor
class Mouse_Sprite(pygame.sprite.Sprite):
    def __init__(self, mousex, mousey, screen_ratios):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/menu/curs.png")
        self.image = pygame.transform.scale(self.image,(40 * screen_ratios[0], 40 * screen_ratios[1]))
        self.rect = self.image.get_rect()
        self.rect.center = (mousex, mousey)
        self.mask = pygame.mask.from_surface(self.image)
    def moving(self, x,y):
        self.rect.center = (x,y)


#Left to do: 
#   Check IP/ Port validity
def Menu(window, screen_size, screen_ratios, window_clock, font_render):
    #json file contains all infos for each button
    #load each button and save for each menu layer
    button_list = json.load(open("Sprites/menu/button_list.json", 'r'))
    Layer_0 = pygame.sprite.Group()#Play + End
    Layer_1 = pygame.sprite.Group()#Host + Join
    Layer_2 = pygame.sprite.Group()#IP + Port
    
    #Load Background
    background = pygame.image.load(f'sprites/menu/BGMenu.png')
    background = pygame.transform.scale(background, (screen_size[0], screen_size[1]))
    background_rect = background.get_rect()
    #Create buttons
    for layer in range(0,3):
        idx = 0
        for button in button_list[f'Layer_{layer}']:
            tmp_button = Menu_button(button["default"], button["text"], screen_size = screen_size, index = idx, font = font_render, assigned_layer= layer)
            if layer == 0:
                Layer_0.add(tmp_button)
            elif layer == 1:
                Layer_1.add(tmp_button)
            elif layer == 2:
                Layer_2.add(tmp_button)
            idx += 1
    #Mouse
    ACTIVE_MOUSE = True
    MOUSE = Mouse_Sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], screen_ratios = screen_ratios)
    #Menu layer management
    Current_layer = 0
    Layers = [Layer_0, Layer_1, Layer_2]
    adress = ["",""]#save user input regarding joining a host (ip, port)
    MENU_RUNNING = True
    while MENU_RUNNING:
        #Same as game loop: update window content, update input, update actions repeat
        #DRAW!
        window_clock.tick(30)
        window.blit(background,background_rect)
        Layers[Current_layer].update(window)
        if ACTIVE_MOUSE:
            window.blit(MOUSE.image, MOUSE.rect)
            mouse_pos = pygame.mouse.get_pos()
            MOUSE.moving(mouse_pos[0], mouse_pos[1])
        #Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#EXIT
                return (False, False, adress[0], adress[1])
            if event.type == pygame.KEYDOWN:
                #Handles escape button
                if event.key == pygame.K_ESCAPE:
                    #If in the main page, exit application
                    if Current_layer == 0:
                        return (False, False, adress[0], adress[1])
                    #if currently the mouse is not activated, activate it again
                    elif ACTIVE_MOUSE == False and Current_layer == 2:
                        #Cancel ip/ port input
                        for sprite in Layers[Current_layer].sprites():
                            sprite.changing == False
                            sprite.update_text(sprite.og_text)
                            sprite.input_string_cpy = ""
                        ACTIVE_MOUSE = True    
                    #Or go back 1 page
                    else:
                        Current_layer -= 1

                #Handle enter button. Only has a job to confirm the ip/port enters (in the last( and 2nd) layer)
                if event.key == pygame.K_RETURN:
                    if ACTIVE_MOUSE and Current_layer == 2:
                        #Check the entered id
                        if adress[0] != "" and adress[1] != "":
                            return (True, False, adress[0], adress[1])
                    #stop changing the user input and save the current number in adress
                    elif not ACTIVE_MOUSE and Current_layer == 2:
                        ACTIVE_MOUSE = True
                        idx = 0
                        for sprite in Layers[Current_layer].sprites():
                            adress[idx] = sprite.return_input()
                            sprite.changing = False
                            idx += 1
                #Backspace
                elif event.key == pygame.K_BACKSPACE and Current_layer == 2 and not ACTIVE_MOUSE:
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        if sprite.changing:
                            sprite.input_string_cpy = sprite.input_string_cpy[:-1]
                #Record every other input as part of the ip/port
                elif Current_layer == 2 and not ACTIVE_MOUSE:
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        if sprite.changing:
                            sprite.input_string_cpy += event.unicode
                            sprite.update_text(sprite.input_string_cpy)       
            #notice mouse clicks. get for the associated button its value to figure out where to go
            if event.type == pygame.MOUSEBUTTONDOWN:
                #For every sprite clicked (its only one)
                for sprite in Layers[Current_layer].sprites():
                    if pygame.sprite.collide_mask(MOUSE, sprite):
                        clicked = sprite.click()

                        #First/Main Layer
                        if Current_layer == 0:
                            if clicked:#Clicked to "Play"
                                Current_layer = 1
                            else:
                                return [False, False, "", ""]#Clicked to "exit"
                        #Host or Joing
                        elif Current_layer == 1:
                            if clicked:
                                return (True, True, "", "")
                            else:
                                Current_layer = 2
                        #In the last layer. clicked on one of the field.
                        #Deactive mouse and enabling text input higher up for the associated sprite
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