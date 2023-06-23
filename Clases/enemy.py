import pygame
from Configuraciones.charge_list_animations import *
from tools import *
from Configuraciones.config_assets import *
import time
from .projectile import Projectile
from Configuraciones.charge_list_animations import *

class Enemy (pygame.sprite.Sprite):
    def __init__(self,initial_position:tuple,animations,speed,count_life):
        super().__init__()
        #Construccion:
        self.frame_animation = 0
        self.speed_animation = 7
        self.animations = animations
        resize_image(self.animations,SIZE_ENEMY_BIRD)
        self.index = 0
        #Lo necesita cualquier elemento:
        self.image = self.animations[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  
        self.is_looking = "derecha"
        #Enemigos tambien requieren
        self.rect_pies = pygame.Rect(initial_position[0],initial_position[1],30,10)
        self.rect_pies.bottom = self.rect.bottom
        self.speed = speed


        self.count_life = count_life
        self.is_alive = True
    def update(self):
        pass




class Bird (Enemy):
    def __init__(self,initial_position:tuple):
        super().__init__(initial_position,enemy_bird_animations,SPEED_BIRD,6)

    def update(self):
        if self.is_looking == "derecha":
            if self.rect.right <= WIDTH: #Debe recibir la plataforma
                self.rect.x += self.speed
                self.animate_motion(tupla_enemy_bird_derecha)
            else:
                self.is_looking = "izquierda"
        elif self.is_looking == "izquierda":
            if self.rect.left >= 0:
                self.rect.x += self.speed*-1
                self.animate_motion(tupla_enemy_bird_izquierda)
            else:
                self.is_looking = "derecha"

        self.image = self.animations[self.index]

    def animate_motion(self,tupla_animaciones):
        """_summary_
        Blitea las animaciones de un objeto
        Args:
            screen (pygame.Surface): Pantalla en la que se muestra
            images (list): Lista de imagenes que hacen la animacion
            key_animations (str): Clave del diccionario que tiene la animacion
        """

        if self.index < tupla_animaciones[0] or self.index > tupla_animaciones[-1]-1:
            self.index = tupla_animaciones[0]
        else:
            self.frame_animation -= 1
            if self.frame_animation < 0:
                self.frame_animation = self.speed_animation 
                self.index+= 1