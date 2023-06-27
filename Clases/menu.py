import pygame
from Configuraciones.config_assets import SIZE_SCREEN
from .button import Button


class Menu ():
    def __init__(self):
        self.font = pygame.font.Font(rf"assets\fonts\gameplay.ttf",40)
        self.background = pygame.image.load(rf"assets\backgrounds\bosque2.jpg")
        self.background = pygame.transform.scale(self.background,(SIZE_SCREEN)) 

        self.menu_pause = pygame.image.load(rf"assets\menu\imagen_pausa.png")
        self.menu_pause = pygame.transform.scale(self.menu_pause,(500,700)) 
        self.rect_menu_pause = self.menu_pause.get_rect()
        # self.rect_menu_pause.x = 400

        self.start = Button((400,400),rf"assets\buttons\start.png",(200,100))
        self.exit = Button((400,400),rf"assets\buttons\exit.png",(150,50))
        self.restart = Button((400,400),rf"assets\buttons\restart.png",(150,50))
        self.reanude = Button((400,400),rf"assets\buttons\quitar_pausa.png",(150,50))

    def draw_text(self,text,color,screen,position):
        image = self.font.render(text,True,color)

        screen.blit(self.background,(0,0))
        # screen.blit(self.menu_pause,(position))
        screen.blit(self.start.image,position)
        screen.blit(self.exit.image,(300,300))

        #screen.blit(image,(position))

