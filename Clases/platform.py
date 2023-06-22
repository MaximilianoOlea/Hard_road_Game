import pygame
from Configuraciones.charge_list_animations import *
from tools import *
from Configuraciones.config_assets import *

class Platform (pygame.sprite.Sprite):
    def __init__(self,path:str,initial_position:tuple,size:tuple):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size) 

        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1] 
        self.floor_collision = pygame.Rect(
        self.rect.left, self.rect.top, self.rect.width, 20)

    def update(self):
        pass
        
    