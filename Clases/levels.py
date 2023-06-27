import pygame

from Configuraciones.charge_list_animations import *

from tools import *

from Configuraciones.config_assets import *

from .platform import *

from .pingu import Pingu

from .enemy import *

from .boss import Boss

class Level (pygame.sprite.Sprite):

    def __init__(self,is_level:int,background:str,music:str):
        super().__init__()
        self.time = 0
        self.key_win = False
        self.is_level = is_level

#Sprites
        self.all_sprites = pygame.sprite.Group()

        self.pingu = Pingu((main_character_x,main_character_y))
        self.all_sprites.add(self.pingu)

        self.sprite_platforms = pygame.sprite.Group()
        self.sprite_enemies = pygame.sprite.Group()
        self.sprite_enemies_wolf = pygame.sprite.Group()
        self.sprite_enemies_ghost = pygame.sprite.Group()

        self.sprite_projectiles = pygame.sprite.Group()
        self.sprite_projectiles_enemies = pygame.sprite.Group()
        self.sprite_items = pygame.sprite.Group()

    
        self.list_platforms = []
        self.fuente = pygame.font.Font(rf"assets\fonts\gameplay.ttf",48)

        self.background = pygame.image.load(background).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    def win (self):
        if not self.sprite_enemies: #Si se eliminaron todos, gana
            self.key_win = True
            self.all_sprites.empty()
            print ("Ganó level")

    def create_platform(self,position:tuple,size:tuple):
        platform = Platform(rf"assets\items\platforms\ice.png",position,size)
        return platform
    

class Level1 (Level):
    def __init__(self):
        super().__init__(1,rf"assets\backgrounds\garden.png",rf"assets\sounds\level\ademas_de_mi.mp3") 
        self.list_platforms = self.create_list_platforms()
        self.create_enemies()

    def create_enemies(self):
        #Bird (3)
        a_enemy = Bird((random.randint(1,WIDTH-10),100)) #Top
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)

        a_enemy = Bird((random.randint(1,400),330)) #MID
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)

        a_enemy = Bird((WIDTH-200,750)) #Bot
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)

        #Ghost (1):
        a_enemy = Ghost((random.randint(600,WIDTH),390)) #Mid
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)
        self.sprite_enemies_ghost.add(a_enemy)

    def create_list_platforms(self):
        list_platform = []
        #Base
        list_platform.append(self.create_platform((0,HEIGHT-20), (WIDTH,30)))

        #Primeros escalones
        list_platform.append(self.create_platform((CENTER_X-200, HEIGHT-200), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((0, HEIGHT-200), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-200), SIZE_PLATFORM_SMALL))

        #MEDIO
        list_platform.append(self.create_platform((CENTER_X-310, HEIGHT-400), SIZE_PLATFORM_MEDIUM))
        list_platform.append(self.create_platform((0, HEIGHT-400), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-400), SIZE_PLATFORM_SMALL))

        #TOP
        list_platform.append(self.create_platform((CENTER_X-310, HEIGHT-600), SIZE_PLATFORM_MEDIUM))
        list_platform.append(self.create_platform((0, HEIGHT-600), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-600), SIZE_PLATFORM_SMALL))

        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform



class Level2 (Level):
    def __init__(self):
        super().__init__(2,rf"assets\backgrounds\grass.png",rf"assets\sounds\level\level2_paulo.mp3") 
        self.list_platforms = self.create_list_platforms()
        self.create_enemies()
        
    def create_enemies(self):
        #Wolf (3)
        a_enemy = Wolf ((100,170)) #Top
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)
        self.sprite_enemies_wolf.add(a_enemy)

        a_enemy = Wolf ((100,300)) #Mid
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)
        self.sprite_enemies_wolf.add(a_enemy)

        a_enemy = Wolf ((100,580)) #bot
        self.all_sprites.add(a_enemy)
        self.sprite_enemies.add(a_enemy)
        self.sprite_enemies_wolf.add(a_enemy)

        #Ghost (3):

        a_enemy = Ghost((random.randint(0,WIDTH),200)) #Top
        self.all_sprites.add(a_enemy)
        self.sprite_enemies.add(a_enemy)
        self.sprite_enemies_ghost.add(a_enemy)

        a_enemy = Ghost((random.randint(0,WIDTH),370)) #Mid
        self.all_sprites.add(a_enemy)
        self.sprite_enemies.add(a_enemy)
        self.sprite_enemies_ghost.add(a_enemy)

        a_enemy = Ghost((random.randint(0,WIDTH),580)) #Bot
        self.sprite_enemies.add(a_enemy)
        self.all_sprites.add(a_enemy)
        self.sprite_enemies_ghost.add(a_enemy)



    def create_list_platforms(self):

        list_platform = []
        #Base
        list_platform.append(self.create_platform((0,HEIGHT-20), (WIDTH,30)))
        #Bot
        list_platform.append(self.create_platform((120, HEIGHT-200), SIZE_PLATFORM_GIGANT))

        #MEDIO
        list_platform.append(self.create_platform((120, HEIGHT-400), SIZE_PLATFORM_GIGANT))
        #TOP
        list_platform.append(self.create_platform((120, HEIGHT-600), SIZE_PLATFORM_GIGANT))


        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform


class Level3 (Level):
    def __init__(self):
        super().__init__(1,rf"assets\backgrounds\bosque2.jpg",rf"assets\sounds\level\level3_midtown.mp3") 
        self.list_platforms = self.create_list_platforms()
        self.create_enemies()

    def create_enemies(self):
        self.boss = Boss((random.randint(0,300),HEIGHT-270))
        self.all_sprites.add(self.boss)   
        self.sprite_enemies.add(self.boss)

    def create_list_platforms(self):

        list_platform = []
        #Base
        list_platform.append(self.create_platform((0,HEIGHT-20), (WIDTH,30)))
        #Bot
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-200), SIZE_PLATFORM_SMALL))
        #MEDIO
        list_platform.append(self.create_platform((CENTER_X-310, HEIGHT-400), SIZE_PLATFORM_MEDIUM))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-400), SIZE_PLATFORM_SMALL))
        #TOP
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-600), SIZE_PLATFORM_SMALL))

        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform
