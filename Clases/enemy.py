import pygame
from Configuraciones.charge_list_animations import *
from tools import *
from Configuraciones.config_assets import *
import time
from .projectile import Projectile
from Configuraciones.charge_list_animations import *
from .item import *
import random



class Enemy (pygame.sprite.Sprite):
    def __init__(self,initial_position:tuple,animations,speed,count_life,size):
        super().__init__()
        #Construccion:
        self.frame_animation = 0
        self.speed_animation = 7
        self.animations = animations
        resize_image(self.animations,size)
        self.index = 0
        #Lo necesita cualquier elemento:
        self.image = self.animations[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  
        self.is_looking = "derecha"
        #Enemigos tambien requieren
        self.rect_pies = pygame.Rect(initial_position[0],initial_position[1],self.rect.width,10)
        self.rect_pies.bottom = self.rect.bottom
        self.speed = speed

        self.rect_ojos = pygame.Rect(self.rect.x,self.rect.y,30,10)
        self.rect_ojos.top = self.rect.top + 30
        self.see = False

        self.count_life = count_life
        self.is_alive = True
    def update(self):
        pass


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
    def see_objective (self,a_objective):
        if self.rect_ojos.top < a_objective.rect.bottom and self.rect_ojos.bottom > a_objective.rect.top:
            self.see = True
        else:
            self.see = False
        return self.see

    def drop_item(self,sprite_items,all_sprites):

        if random.randint(1,2) == 1: #Probabilidad de que dropeen los enemigos
            if random.randint(1,2) == 1: #50% de fish 50% de boots
                item = Item_fish ((self.rect.x,self.rect.y))
                sprite_items.add(item)
                all_sprites.add(item)
            else:
                item = Item_boots ((self.rect.x,self.rect.y))
                sprite_items.add(item)
                all_sprites.add(item)

class Bird (Enemy):
    def __init__(self,initial_position:tuple):
        super().__init__(initial_position,enemy_bird_animations,SPEED_BIRD,COUNT_LIFE_BIRD,SIZE_ENEMY_BIRD)

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


class Ghost (Enemy):
    def __init__(self,initial_position:tuple):
        super().__init__(initial_position,enemy_ghost_animations,SPEED_GHOST,COUNT_LIFE_GHOST,SIZE_ENEMY_GHOST)
        self.is_doing = "camina"
        self.time_reload = 4
        self.last_shot_time = 0
        self.count_projectile = 5
    def update(self):

        if self.count_life > 0:
            if self.is_looking == "derecha":
                if self.rect.right <= WIDTH: #Debe recibir la plataforma
                    self.rect.x += self.speed
                    self.rect_ojos.x += self.speed
                    if self.is_doing != "dispara":
                        self.animate_motion(tupla_enemy_ghost_derecha)
                    else:
                        self.animate_motion(tupla_enemy_ghost_dispara_derecha)
                else:
                    self.is_looking = "izquierda"
            elif self.is_looking == "izquierda":
                if self.rect.left >= 0:
                    self.rect.x += self.speed*-1
                    self.rect_ojos.x += self.speed*-1
                    if self.is_doing != "dispara":
                        self.animate_motion(tupla_enemy_ghost_izquierda)
                    else:
                        self.animate_motion(tupla_enemy_ghost_dispara_izquierda)
                else:
                    self.is_looking = "derecha"

            self.image = self.animations[self.index]
        else:
            if self.is_looking == "derecha":
                self.animate_motion(tupla_enemy_ghost_muere_derecha)
            else:
                self.is_looking == "izquierda"
                self.animate_motion(tupla_enemy_ghost_muere_izquierda)
        self.image = self.animations[self.index]

    def shoot_projectile(self,pos_x, pos_y,direction_projectile:str,sprites_projectiles,all_sprite):
        current_time = time.time() # Obtener el tiempo actual en segundos
        # Si desde el ultimo tiro paso 1 segundo habilito a que tire de nuevo
        if current_time - self.last_shot_time >= self.time_reload and self.count_projectile > 0:
            #Actualizar ultimo tiro
            self.last_shot_time = current_time  
            un_projectile = Projectile(
            rf"assets\enemies\boss\fireboss\power\flame_shoot-PhotoRoom.png-PhotoRoom.png",(pos_x, pos_y),
            SIZE_PROJECTILE_ENEMY,SPEED_PROJECTILE_ENEMY,direction_projectile,True)
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)
            self.count_projectile -= 1
            self.is_doing = "dispara"
            if self.count_projectile == 0:
                self.count_projectile = 5   


class Wolf (Enemy):
    def __init__(self,initial_position:tuple):
        super().__init__(initial_position,enemy_wolf_animations,SPEED_WOLF,COUNT_LIFE_WOLF,SIZE_ENEMY_WOLF)
        self.is_in_floor = False
        self.gravity = 5
        self.is_falling = False
        self.speed_buff = 5
    def update(self):
        if self.is_looking == "derecha":
            if self.rect.right <= WIDTH: #Debe recibir la plataforma
                self.rect.x += self.speed
                self.rect_ojos.x += self.speed
                self.rect_pies.x += self.speed
                self.animate_motion(tupla_enemy_wolf_derecha)
            else:
                self.is_looking = "izquierda"
        elif self.is_looking == "izquierda":
            if self.rect.left >= 0:
                self.rect.x += self.speed*-1
                self.rect_ojos.x += self.speed*-1
                self.rect_pies.x += self.speed*-1

                self.animate_motion(tupla_enemy_wolf_izquierda)
            else:
                self.is_looking = "derecha"

        if not self.is_in_floor or self.is_falling:
            self.rect.y += self.gravity
            self.rect_ojos.y += self.gravity
            self.rect_pies.y += self.gravity

        self.image = self.animations[self.index]


    def check_collision_floor(self,floor_impact):
        flag = False
        floor_impacted = None 

        for platform in floor_impact:
            if self.rect_pies.colliderect(platform):
                flag = True
                floor_impacted = platform.rect.top

        if flag:
            self.rect.bottom = floor_impacted
            self.rect_pies.bottom = floor_impacted
            self.rect_ojos.top = self.rect.top + 30 

            self.movement_y = 0
            self.is_in_floor = True
        else:
            self.is_falling = True
    

