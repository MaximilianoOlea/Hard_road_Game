import pygame
from Configuraciones.config_assets import SIZE_SCREEN
from .button import Button


class Menu ():
    def __init__(self):
        self.font = pygame.font.Font(rf"assets\fonts\gameplay.ttf",40)
        self.background = pygame.image.load(rf"assets\backgrounds\bosque2.jpg")
        self.background = pygame.transform.scale(self.background,(SIZE_SCREEN)) 
    #Main
        self.start = Button((850,320),rf"assets\buttons\start.png",(150,80))
        self.quit = Button((850,420),rf"assets\buttons\exit.png",(150,50))
        self.background_main = pygame.image.load(rf"assets\backgrounds\Bosque.jpg")
    #Pause
        self.reanude = Button((850,400),rf"assets\buttons\quitar_pausa.png",(150,50))
        self.restart = Button((850,500),rf"assets\buttons\restart.png",(150,50))
        self.exit = Button((850,600),rf"assets\buttons\exit.png",(150,50))
        
    #WIN:
        self.back = Button((850,600),rf"assets\buttons\back.png",(150,50))
    def draw_text(self,text,color,screen,position):
        image = self.font.render(text,True,color)
        screen.blit(image,(position))

