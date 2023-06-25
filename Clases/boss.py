import pygame

from .enemy import Enemy

from Configuraciones.charge_list_animations import *

from tools import *

from Configuraciones.config_assets import *

import time

from .projectile import Ice_shoot,Water_shoot,Fire_shoot

from Configuraciones.charge_list_animations import *

from .item import *

import random
class Boss (Enemy):
    def __init__(self,initial_position:tuple):
        super().__init__(initial_position,boss_animations,SPEED_BOSS,COUNT_LIFE_BOSS,SIZE_BOSS)
        self.time_reload_ice = 4
        self.time_reload_fire = 4
        self.time_reload_dash = 10
        self.last_shot_ice = 0
        self.last_shot_fire = 0
        self.last_dash = 0
        self.count_projectile = 5
        self.attacked_water = False
        self.fases = 0
        self.is_alive = True
        self.rect_ojos.x = self.rect.right
        self.up = True
        self.right = True
        self.is_doing = "volar"
    def update(self):
        
        if self.count_life < COUNT_LIFE_BOSS - 20:
            self.fases = 1
            self.image = self.animations[1]
        if self.count_life < COUNT_LIFE_BOSS - 30:
            self.fases = 2
            self.image = self.animations[2]
        if self.count_life < COUNT_LIFE_BOSS - 100:
            self.fases = 3
            self.image = self.animations[3]
        if self.count_life < COUNT_LIFE_BOSS - 140 and self.is_doing == "volar":
            self.fases = 4
            if self.rect.top >= 0 and self.up:
                self.rect.y -= 3
                self.rect_ojos.y -= 3
            else:
                self.up = False
                if self.rect.bottom <= HEIGHT - 100:
                    self.rect.y += 3
                    self.rect_ojos.y +=3
                else:
                    self.up = True
        if self.count_life < COUNT_LIFE_BOSS - 200:
            self.fases = 5
            if self.rect.right <= WIDTH and self.right == True and self.is_doing == "avalanzar" :
                self.rect.x += 12
                self.rect_ojos.x +=12
            else:
                self.right = False

                if self.rect.left >= 0:
                    self.rect.x -= 5
                    self.rect_ojos.x -=5
                else:
                    self.right = True
                    self.is_doing = "volar"

        # if self.count_life <= 0:
        #     self.is_alive = False


    def attack_ice (self,sprites_projectiles,all_sprite):
        if self.fases == 1 or  self.fases == 2 or self.fases == 5:
            current_time = time.time() # Obtener el tiempo actual en segundos
            # Si desde el ultimo tiro paso 1 segundo habilito a que tire de nuevo
            if current_time - self.last_shot_ice >= self.time_reload_ice:
                #Actualizar ultimo tiro
                self.last_shot_ice = current_time  
                self.create_ice_shot(sprites_projectiles,all_sprite,10)

    
    def attack_water (self,sprites_projectiles,all_sprite):

        if not self.attacked_water and self.fases == 2:
            self.attacked_water = True
            un_projectile = Water_shoot((1,HEIGHT-80))
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)
            dos_projectile = Water_shoot((WIDTH-20,HEIGHT-80))
            sprites_projectiles.add(dos_projectile)
            all_sprite.add(dos_projectile)


    def attack_fire (self,sprites_projectiles,all_sprite):

        if self.fases == 3:
            current_time = time.time() # Obtener el tiempo actual en segundos
            # Si desde el ultimo tiro paso 1 segundo habilito a que tire de nuevo
            if current_time - self.last_shot_fire >= self.time_reload_fire :
                #Actualizar ultimo tiro
                self.last_shot_fire = current_time 
                self.create_fire_shot(sprites_projectiles,all_sprite,3)




    
    def create_fire_shot (self,sprites_projectiles,all_sprite,count):

        for i in range(count):
            un_projectile = Fire_shoot((0,random.randint(200,HEIGHT-100)))
            un_projectile.speed = random.randint(7,12)
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)

    def attack_one_fire (self,sprites_projectiles,all_sprite,pos_initial):
        current_time = time.time() # Obtener el tiempo actual en segundos
        # Si desde el ultimo tiro paso 1 segundo habilito a que tire de nuevo
        if current_time - self.last_shot_fire >= self.time_reload_fire :
            #Actualizar ultimo tiro
            self.last_shot_fire = current_time 
            if self.fases == 4 or self.fases == 5:
                self.create_one_fire_shot(sprites_projectiles,all_sprite,pos_initial)

    def create_one_fire_shot (self,sprites_projectiles,all_sprite,pos_initial):

            un_projectile = Fire_shoot(pos_initial)
            un_projectile.speed = 20
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)

    def create_ice_shot (self,sprites_projectiles,all_sprite,count):

        for i in range(count):
            un_projectile = Ice_shoot((random.randint(10,WIDTH-5),-20))
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)

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
                self.frame_animation = 30
                self.index+= 1

    def dash (self):

        current_time = time.time() # Obtener el tiempo actual en segundos
        if current_time - self.last_dash >= self.time_reload_dash :

            if self.fases == 5:
                self.last_dash = current_time 
                self.is_doing = "avalanzar"