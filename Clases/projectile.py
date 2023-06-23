import pygame
from Configuraciones.config_assets import WIDTH

class Projectile (pygame.sprite.Sprite):
    def __init__(self,path:str,initial_position:tuple,size,speed_proyectile:int,direction_projectile:str):
        super().__init__()

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size) 

        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  
        self.speed = speed_proyectile
        self.direction_projectile = direction_projectile
        
        self.impacted = False
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
            self.play_sound(rf"assets\sounds\pingu\proyectile_collide.mp3")
        return self.impacted
    
    def update(self):
        if self.direction_projectile == "derecha":
            self.rect.x += self.speed
        elif self.direction_projectile == "izquierda":
            self.rect.x += self.speed*-1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.kill()


    def play_sound (self,sound):
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()