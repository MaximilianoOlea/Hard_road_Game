import pygame
from Configuraciones.charge_list_animations import *
from tools import *
from Configuraciones.config_assets import *
import time
from .projectile import Projectile

class Pingu (pygame.sprite.Sprite):
    def __init__(self,initial_position:tuple):
        super().__init__()
        #Construccion:
        self.frame_animation = 0
        self.speed_animation = 7
        self.animations = pingu_animations
        resize_image(self.animations,SIZE_MAIN_CHARACTER)
        self.index = 0
        #Lo necesita cualquier elemento:
        self.image = self.animations[self.index]
        self.image = self.animations[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  

        self.pos_respaw = initial_position

        #Enemigos tambien requieren
        self.rect_pies = pygame.Rect(initial_position[0],initial_position[1],self.rect.width,10)
        self.rect_pies.bottom = self.rect.bottom

        #Movimiento: 
        self.speed = SPEED_MAIN_CHARACTER
        #Salto
        self.gravity = GRAVITY_MAIN_CHARACTER
        self.jump_power = JUMP_POWER_MAIN_CHARACTER
        self.limit_speed_fall = JUMP_POWER_MAIN_CHARACTER
        self.is_jumping = False
        self.is_in_floor = True
        self.movement_y = 0

        self.is_looking = "derecha" #Comienza mirando a la derecha
        self.is_doing = "quieto" #Comienza quieto

        self.is_falling = False

        self.score = 0
        self.count_life = 3
        self.count_projectile = 5
        self.is_alive = True  
        self.last_shot_time = 0
        self.time_reload = SPEED_SHOOT_RELOAD

        #Prueba
        self.bajar_plataforma = False


        self.respawn_time = 3  # Tiempo de espera antes de resucitar en segundos
        self.respawn_timer = None
        self.impacted = False
        self.vulnerable = True
    def update(self):
        #Movimientos laterales
        if self.is_alive:
            match self.is_doing:
                case "quieto":
                    if not self.is_jumping and self.is_in_floor:
                        if self.is_looking == "derecha":
                        #ANIMACION
                            self.animate_motion(tupla_quieto_derecha)
                        elif self.is_looking == "izquierda":
                            self.animate_motion(tupla_quieto_izquierda)
                    else:
                        if self.is_looking == "derecha":
                            self.animate_motion(tupla_salta_derecha)
                        elif self.is_looking == "izquierda":
                            self.animate_motion(tupla_salta_izquierda)
                        #---------------------------
                case "derecha":
                    self.is_looking = "derecha"
                    if not self.is_jumping and self.is_in_floor:
                        self.animate_motion(tupla_camina_derecha)
                    self.move(self.speed)
                case "izquierda":
                    self.is_looking = "izquierda"
                    if not self.is_jumping and self.is_in_floor:
                        self.animate_motion(tupla_camina_izquierda)
                    self.move(self.speed,True,False)

                case "salta":
                    if not self.is_jumping and self.is_in_floor:
                        self.is_jumping = True
                        self.is_in_floor = False

                        self.move(self.jump_power*-1,False)

                case "dispara":
                    if not self.is_jumping:
                        if self.is_looking == "derecha":
                            self.animate_motion(tupla_dispara_derecha)
                        elif self.is_looking == "izquierda":
                            self.animate_motion(tupla_dispara_izquierda)

            self.image = self.animations[self.index]
        else: #Perdio una vida
            self.rect.y -= 1
            if self.is_looking == "derecha":
                self.image = self.animations[32] #Index de la muerte
            elif self.is_looking == "izquierda":
                self.image = self.animations [33]

        if not self.is_alive:
            if self.count_life <= 0:
                self.kill()
            else:
                if self.respawn_timer is None:
                    self.respawn_timer = time.time() + self.respawn_time
                elif time.time() >= self.respawn_timer:
                    self.revive()
                    self.rect.x = self.pos_respaw[0]
                    self.rect.y = self.pos_respaw[1]
                    self.rect_pies.x = self.pos_respaw[0]
                    self.rect_pies.y = self.rect.bottom 
                    self.respawn_timer = None

        self.jump()
    # Restringir movimientos:

    def move(self, speed: int, lateral_movement: bool = True, right_movement: bool = True):  # OK
        """_summary_
            Mueve el rectangulo que conforman al elemento del juego
        Args:
            speed (int): Velocidad en la que se desplaza
            lateral_movement (bool, optional): True = Se mueve de forma lateral | False = Se mueve de forma vertical
        """
        if lateral_movement:
            if right_movement:
                if not self.limit_moves(WIDTH,"derecha"):
                    self.rect.x += speed
                    self.rect_pies.x += speed
            else:
                if not self.limit_moves(0,"izquierda"):
                    self.rect.x += speed*-1
                    self.rect_pies.x += speed*-1

        else:
            self.movement_y = speed



    def _limit_moves_right(self, limit_right):
        limit = True

        if self.rect.right >= limit_right:
            limit = True
        else:
            limit = False

        return limit

    def _limit_moves_left(self, limit_left):
        limit = True

        if self.rect.left <= limit_left:
            limit = True
        else:
            limit = False

        return limit

    def _limit_moves_top(self, limit_top):
        limit = True

        if self.rect.top <= limit_top:
            limit = True
        else:
            limit = False

        return limit

    def limit_moves(self, limit, option: str) -> bool:
        """_summary_

        Args:
            limit (_type_): El limite que no debe pasar
            option (str): Direccion en la que se mueve

        Returns:
            bool: Devuelve false si no se alcanzo el limite
        """
        match option:
            case "derecha":
                return self._limit_moves_right(limit)
            case "izquierda":
                return self._limit_moves_left(limit)
            case "top":
                return self._limit_moves_top(limit)
            

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

    def jump(self):
        if not self.is_in_floor or self.is_falling:
            self.rect_pies.y += self.movement_y
            self.rect.y += self.movement_y

            if self.movement_y + self.gravity < self.limit_speed_fall:
                self.movement_y += self.gravity
                self.rect_pies.y += self.gravity
                if self.movement_y > 0:
                    self.is_falling = True
                else:
                    self.is_falling = False
 

        self.__jump_draw()

    def __jump_draw(self):
        if self.is_jumping or not self.is_in_floor:
            if self.is_looking == "derecha":
                self.animate_motion(tupla_salta_derecha)
            else: 
                self.animate_motion(tupla_salta_izquierda)

    
    def check_collision_floor(self,floor_impact):
        flag = False
        floor_impacted = None 

        for platform in floor_impact:
            if self.rect_pies.colliderect(platform):
                flag = True
                floor_impacted = platform.rect.top

        if flag:
            if self.is_falling:
                self.rect.bottom = floor_impacted
                self.rect_pies.bottom = floor_impacted
                self.movement_y = 0
                self.is_jumping = False
                self.is_in_floor = True
                # self.is_falling = False
        else:
            self.is_falling = True  # Si no hay colisión, permitir que caiga
        # if not flag and self.is_in_floor:
        #     self.is_in_floor = False
            # self.bajar_plataforma = False
            # self.is_falling = True 
            print ("entro")

#Disparar

    def shoot_projectile_pingu(self,pos_x, pos_y,direction_projectile:str,sprites_projectiles,all_sprite):
        current_time = time.time() # Obtener el tiempo actual en segundos
        
        # Si desde el ultimo tiro paso 1 segundo habilito a que tire de nuevo
        if current_time - self.last_shot_time >= self.time_reload and self.count_projectile > 0:
            #Actualizar ultimo tiro
            self.last_shot_time = current_time  
            un_projectile = Projectile(
            rf"assets\items\pingu_proyectile.png",(pos_x, pos_y),SIZE_PROJECTILE,15,direction_projectile,True)
            sprites_projectiles.add(un_projectile)
            all_sprite.add(un_projectile)
            self.count_projectile -= 1
            if self.count_projectile == 0:
                self.count_projectile = 5

    def dead (self,enemy):
        if self.rect.colliderect(enemy) and self.is_alive and not self.impacted:
            self.is_alive = False
            if self.count_life >= 0:
                self.count_life -= 1
            self.play_sound("assets\sounds\menu\dead.mp3")
    def revive (self):
        if not self.is_alive:
            self.is_alive = True
            self.is_in_floor = True
            self.speed = SPEED_MAIN_CHARACTER
            self.time_reload = SPEED_SHOOT_RELOAD
            self.speed_animation = SPEED_ANIMATION
        
    def play_sound(self,path):
        sound = pygame.mixer.Sound(path)
        sound.play()