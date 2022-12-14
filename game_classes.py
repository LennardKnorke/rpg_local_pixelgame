import pygame
import os
import json

class Game_Application():
    pass
class Player(pygame.sprite.Sprite):
    pass

class Menu_button(pygame.sprite.Sprite):
    def __init__(self, button_type, text, SCREEN_SIZE, index, FONT, assigned_layer):
        pygame.sprite.Sprite.__init__(self)
        self.button_type = button_type
        self.button_text = text
        self.menu_layer = assigned_layer
        if self.button_type == "default":
            #Load default picture and adjust size
            self.image = pygame.image.load(f"sprites/menu/{self.button_type}.png")
            self.image = pygame.transform.scale(self.image, (SCREEN_SIZE[0] / 5,SCREEN_SIZE[1] / 10))
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / (3 - index))
            #Load text for a default button
            self.button_text = FONT.render(self.button_text, False, (0,0,0))
            self.button_text_rect = self.button_text.get_rect()
            self.button_text_rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / (3 - index))
            self.mask = pygame.mask.from_surface(self.image)
        self.selected = False
    def hovering(self):
        if self.selected:
            pass
        else:
            pass
    def click (self):
        pass
    def draw_button(self, SCREEN):
        SCREEN.blit(self.button_text, self.button_text_rect)
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
    def update(self, SCREEN):
        self.hovering()
        self.draw(SCREEN)
        self.draw_button(SCREEN)
        
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
#Run the main menu, return next desired state
#First layers. Play or exit
#Adventure or vs mode
#Host or Join
#Enter IP, port
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

    for layer in range(0,5):
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
    MOUSE = Mouse_Sprite(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], SCREEN_SIZE=SCREEN_SIZE)
    Current_layer = 0
    Layers = [Layer_0,Layer_1, Layer_2,Layer_3,Layer_4]
    while MENU_RUNNING:
        CLOCK.tick(30)
        SCREEN.blit(background,background_rect)
        
        Layers[Current_layer].update(SCREEN)
        SCREEN.blit(MOUSE.image, MOUSE.rect)
        mouse_pos = pygame.mouse.get_pos()
        MOUSE.moving(mouse_pos[0], mouse_pos[1])
        for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
            sprite.hovering()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if Current_layer == 0:
                        return 0
                    else:
                        Current_layer -= 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for sprite in pygame.sprite.spritecollide(MOUSE, Layers[Current_layer], False):
                        sprite.click()
        pygame.display.update()

def adventure():
    pass