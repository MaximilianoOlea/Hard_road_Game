import pygame
from Configuraciones.config_assets import *
import random
class Projectile (pygame.sprite.Sprite):
    def __init__(self,path:str,initial_position:tuple,size,speed_proyectile:int,direction_projectile:str,is_eliminate:bool):
        super().__init__()

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size) 

        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  
        self.speed = speed_proyectile
        self.direction_projectile = direction_projectile
        self.impacted = False
        self.movement_y = 0
        self.is_eliminate = is_eliminate

    def check_objective (self,a_objective)->bool:
        """Devuelve verdadero si colisiona con un objetivo
        Args:
            a_objective (_type_): _description_
        Returns:
            bool: _description_
        """
        if not self.impacted and self.rect.colliderect(a_objective):
            a_objective.count_life -= 1
            self.impacted = True
            self.kill()
            self.play_sound()
        return self.impacted
    
    def update(self):
        if self.direction_projectile == "derecha":
            self.rect.x += self.speed
        elif self.direction_projectile == "izquierda":
            self.rect.x += self.speed*-1
        elif self.direction_projectile == "abajo":
            self.rect.y = 1
            self.rect.y += self.movement_y
            if self.movement_y + self.speed < HEIGHT - 70:
                self.movement_y += self.speed
            if self.rect.bottom >= HEIGHT and self.is_eliminate:
                self.kill()

        if self.is_eliminate:
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.kill()
        else:
            if self.rect.left <= 0:
                self.direction_projectile = "derecha"
            elif self.rect.right >= WIDTH:
                self.direction_projectile = "izquierda"


    def play_sound(self):
        sound = pygame.mixer.Sound(rf"assets\sounds\pingu\proyectile_collide.mp3")
        sound.play()


class Ice_shoot (Projectile):
    def __init__(self,initial_position:tuple):
        super().__init__(rf"assets\enemies\boss\iceboss\powers\0.png",initial_position,SIZE_PROJECTILE_BOSS,SPEED_PROJECTILE_BOSS_ICE,"abajo",True)


class Water_shoot (Projectile):
    def __init__(self,initial_position:tuple):
        super().__init__(rf"assets\enemies\boss\waterboss\power\1.png",initial_position,(80,60),3,"derecha",False)

class Fire_shoot (Projectile):
    def __init__(self,initial_position:tuple):
        super().__init__(rf"assets\enemies\boss\iceboss\powers\shoot.png",initial_position,(70,70),SPEED_PROJECTILE_BOSS_FIRE,"derecha",True)


