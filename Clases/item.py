import pygame

from Configuraciones.config_assets import HEIGHT,SIZE_ITEM
class Item (pygame.sprite.Sprite):
    def __init__(self,path:str,initial_position:tuple,size):
        super().__init__()

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size) 

        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]  
        self.impacted = False


    def update(self):
        pass

    def check_collision (self,a_objective)->bool:
        """Devuelve verdadero si colisiona con un objetivo
        Args:
            a_objective (_type_): _description_
        Returns:
            bool: _description_
        """
        if not self.impacted and self.rect.colliderect(a_objective):
            self.impacted = True
            a_objective.score += 1000
            self.kill()
            self.play_sound()
        return self.impacted
    
    def play_sound(self):
        sound = pygame.mixer.Sound(rf"assets\sounds\items\item_pez.mp3")
        sound.play()

class Item_fish (Item):
    def __init__(self,initial_position):
        super().__init__("assets\items\item_pez_speed_shot.png",initial_position,SIZE_ITEM)
        self.speed_shoot_buff = 0.1

    def update(self):
        pass
    def buff (self,a_objective):
        if self.check_collision(a_objective):
            a_objective.time_reload = self.speed_shoot_buff

class Item_boots (Item):
    def __init__(self,initial_position):
        super().__init__("assets\items\item_bota_speed.png",initial_position,SIZE_ITEM)
        self.speed_buff = 11
        self.speed_animation_buff = 3
    def update(self):
        pass
    def buff (self,a_objective):
        if self.check_collision(a_objective):
            a_objective.speed = self.speed_buff
            a_objective.speed_animation = self.speed_animation_buff

#LOGICA PARA LOS PINCHES DE HIELO DE ARRIBA QUE CAEN

    # def update(self):
    #     self.rect.y = 1
    #     self.rect.y += self.movement_y

    #     if self.movement_y + self.gravity < HEIGHT - 100:
    #         self.movement_y += self.gravity
