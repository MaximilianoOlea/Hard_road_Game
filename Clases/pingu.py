import pygame
from Configuraciones.charge_list_animations import *
from tools import *
from Configuraciones.config_assets import *

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
        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  

        #Movimiento: 
        self.speed = SPEED_MAIN_CHARACTER
        #Salto
        self.gravity = GRAVITY_MAIN_CHARACTER
        self.jump_power = JUMP_POWER_MAIN_CHARACTER
        self.limit_speed_fall = JUMP_POWER_MAIN_CHARACTER
        self.is_jumping = False
        self.is_in_floor = False
        self.movement_y = 0

        self.is_looking = "derecha" #Comienza mirando a la derecha
        self.is_doing = "quieto" #Comienza quieto

        self.is_falling = False

        self.score = 0
        self.count_life = 1
        self.count_projectile = 5
        self.is_alive = True  
        self.last_shot_time = 0
        self.time_reload = 1

        #Prueba
        self.bajar_plataforma = False
        self.rect_pies = pygame.Rect(initial_position[0],initial_position[1],30,10)
        self.rect_pies.bottom = self.rect.bottom

    def update(self):
        #Movimientos laterales
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
                        "anima"
                        pass
                    elif self.is_looking == "izquierda":
                        pass
                        #anima
        self.image = self.animations[self.index]

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
        if not self.is_in_floor:
            self.rect_pies.y += self.movement_y
            self.rect.y += self.movement_y

            # self.caer()
            if self.movement_y + self.gravity < self.limit_speed_fall:
                self.movement_y += self.gravity
                self.rect_pies.y += self.gravity
                if self.movement_y > 0:
                    self.is_falling = True
                else:
                    self.is_falling = False
        else:
            self.is_falling = False

        self.__jump_draw()

    def __jump_draw(self):
        if self.is_jumping or not self.is_in_floor:
            if self.is_looking == "derecha":
                self.animate_motion(tupla_salta_derecha)
            else: 
                self.animate_motion(tupla_salta_izquierda)

    def caer(self):
        if self.is_falling:
            self.movement_y += self.gravity 
        if not self.is_jumping and not self.is_in_floor:
            self.is_falling = True
    
    def check_collision_floor(self,floor_impact):

        if self.rect_pies.colliderect(floor_impact):
            if self.is_falling:
                self.rect.bottom = floor_impact.top
                self.rect_pies.bottom = floor_impact.top
                self.movement_y = 0
                self.is_jumping = False
                self.is_in_floor = True
                self.limit_speed_fall = floor_impact.top
                print (self.limit_speed_fall)
        else:
            self.bajar_plataforma = True
            self.is_falling = True





    # def verificar_colision_piso(self,piso):  
        
    #     if self.rect_pies.colliderect(piso):
    #         self.is_falling = False
    #         self.limit_speed_fall = piso.top
    #     else:
    #         self.is_falling = True

    # def caida (self):
    #     if self.is_falling :
    #         if self.movement_y + self.gravity < self.limit_speed_fall:  
