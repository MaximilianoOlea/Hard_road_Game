import pygame

import sys 

import random

from Configuraciones.config_assets import *

from Configuraciones.mode import *

from Configuraciones.diccionarios_assets import *

from Configuraciones.charge_list_animations import *

from .pingu import Pingu

from .platform import Platform

from .enemy import *
from .boss import Boss

from .item import *


class Game:
    def __init__(self, size_screen: tuple, name_game: str,icon_path:str):

        pygame.init()
        self.screen = pygame.display.set_mode((size_screen))
        pygame.display.set_caption(name_game)
        self.clock = pygame.time.Clock()
        icon = pygame.image.load (icon_path)
        pygame.display.set_icon(icon)
        
        # Estado del juego
        self.playing = False
        self.finished = True
        self.pause = False
        # ----------------------------------------------------

        #Test:
        self.background = pygame.image.load(rf"assets\backgrounds\garden.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        #Sprites
        self.all_sprites = pygame.sprite.Group()

        self.pingu = Pingu((main_character_x,main_character_y))
        self.all_sprites.add(self.pingu)

        self.sprite_platforms = pygame.sprite.Group()
        self.sprite_enemies = pygame.sprite.Group()
        self.sprite_projectiles = pygame.sprite.Group()
        self.sprite_projectiles_enemies = pygame.sprite.Group()
        self.sprite_items = pygame.sprite.Group()

#ENEMIGOS
        self.enemy_bird = Bird((WIDTH-250,750))
        self.enemy_ghost = Ghost((random.randint(600,WIDTH),370))
        self.enemy_wolf = Wolf ((random.randint(1,WIDTH-10),random.randint(140,800)))
        self.boss = Boss((random.randint(1,30),HEIGHT-270))

        self.all_sprites.add(self.enemy_bird)
        self.all_sprites.add(self.enemy_ghost)
        self.all_sprites.add(self.enemy_wolf)
        self.all_sprites.add(self.boss)

        self.sprite_enemies.add(self.enemy_bird)
        self.sprite_enemies.add(self.enemy_ghost)
        self.sprite_enemies.add(self.enemy_wolf)
        self.sprite_enemies.add(self.boss)

        #self.lista_plataformas = self.create_list_platforms()
        self.lista_plataformas = self.create_list_platforms()

        self.fuente = pygame.font.Font(rf"assets\fonts\gameplay.ttf",48)

        pygame.mixer.init()
        pygame.mixer.music.load(rf"assets\sounds\level\level3_midtown.mp3")
        pygame.mixer.music.play(-1)


# ------------------------------------------------------


# Estados del juego


    def start(self, fps: int):
        """_summary_
            Comienza el juego
        Args:
            fps (int): Velocidad en la que correrá el juego
        """
        self.playing = True
        self.finished = False

        while self.playing:
            self.clock.tick(fps)
            self.handle_event(self.background)
    def exit(self):
        """Salir definitivamente del juego
        """
        pygame.quit()
        sys.exit()

    def finished_game(self):
        """Terminar la partida pero no salir del juego
        """
        self.playing = False
        self.finished = True

    def game_over(self):
        """Termina la partida pero no el juego
        """
        #self.finalizado = True
        self.show_screen_game_over()

# -------------------

    def reset(self):  # Debe recibir el nivel
        pass

    # Muestra la pantalla de partida perdida
    def show_screen_game_over(self):

        texto = self.fuente.render("Game Over",True,(0,0,255))
        rect_texto = texto.get_rect()
        rect_texto.center = CENTER 
        self.screen.fill((0,0,0))
        self.screen.blit(texto,rect_texto)
        pygame.display.flip()

    def draw_score(self,score):

        texto = self.fuente.render(f"Score:{score}",True,(ROJO))
        rect_texto = texto.get_rect()
        rect_texto.x = 10
        self.screen.blit(texto,rect_texto)

    def draw_life(self,count_life):
        icon_vida = pygame.image.load(rf"assets\menu\life.png")
        icon_vida = pygame.transform.scale(icon_vida, (40,60)) 
        rect_icon_vida = icon_vida.get_rect()
        rect_icon_vida.x = WIDTH-150
        self.screen.blit(icon_vida,rect_icon_vida)
        texto = self.fuente.render(f"{count_life}",True,(AZUL))
        rect_texto = texto.get_rect()
        rect_texto.x = rect_icon_vida.x + 60
        self.screen.blit(texto,rect_texto)


    def show_screen_pause(self):
        # Pausa el juego,muestra Opcion de Reinicio | volver al juego |Salir al menu principal
        self.pause = not self.pause
        self.play_sound(rf"assets\sounds\menu\pause.mp3")
        return self.pause
#Manejador de eventos:
    def handle_event(self,background):
        """_summary_
        Controla los eventos del juego
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    change_mode()  # Modo admid (Ver rectangulos de colision)
                elif evento.key == pygame.K_RETURN:
                    self.show_screen_pause()
                elif evento.key == pygame.K_j or evento.key == pygame.K_z:
                    if not self.pause and self.pingu.is_alive:
                        self.pingu.is_doing = "dispara"              
                        self.pingu.shoot_projectile_pingu(
                        self.pingu.rect.x,self.pingu.rect.y,self.pingu.is_looking,self.sprite_projectiles,self.all_sprites)
                elif evento.key == pygame.K_DOWN:
                    if self.pingu.is_in_floor:
                        self.pingu.bajar_plataforma = True
                        self.pingu.is_in_floor = False
                elif evento.key == pygame.K_p: #Agregar vida
                    if self.pingu.count_life < 99:
                        self.pingu.count_life+=1
                        self.play_sound(rf"assets\sounds\menu\life.mp3")


        if not self.pause:
            if self.pingu.is_alive:
                self.controller_movement()
            self.render_screen(background)
            #Si cae sobre un enemigo
#------------------------------------------------------

    def render_screen(self, background):#Object_game seran una lista
        """_summary_
        Actualiza los elementos de la pantalla

        Args:
            screen (_type_): Pantalla en la que va a blitearse
            object_game (list): Todos los elementos del juego (Lista de diccionarios)
        """

        self.screen.blit(background,(ORIGIN))   
        self.draw_score(self.pingu.score)
        self.draw_life(self.pingu.count_life)

        # if not self.sprite_enemies:
        #     self.create_enemies()


        self.pingu.check_collision_floor(self.lista_plataformas)
        self.enemy_wolf.check_collision_floor(self.lista_plataformas)

#Impacto de disparo hacia un enemigo:
        for enemy in self.sprite_enemies:
            for projectile in self.sprite_projectiles:
                if projectile.check_objective(enemy):
                    self.pingu.score += 100
            if enemy.count_life <= 0:
                enemy.kill()
                self.all_sprites.remove(enemy)
                self.sprite_enemies.remove(enemy)
                enemy.drop_item(self.sprite_items,self.all_sprites)

        for projectile in self.sprite_projectiles_enemies:
            if projectile.impacted:
                enemy.drop_item(self.sprite_items,self.all_sprites)
#Impacto con enemigo (muerte)
        for enemy in self.sprite_enemies:
            self.pingu.dead(enemy)
        for projectile_enemy in self.sprite_projectiles_enemies:
            self.pingu.dead(projectile_enemy)    

        #Ghost:
        if self.enemy_ghost.count_life > 0:
            if self.enemy_ghost.see_objective(self.pingu):
                if self.enemy_ghost.is_looking == "derecha":
                    if self.enemy_ghost.rect.right < self.pingu.rect.left:
                        self.enemy_ghost.shoot_projectile(
                        self.enemy_ghost.rect.x+10,self.enemy_ghost.rect.y+10,self.enemy_ghost.is_looking,self.sprite_projectiles_enemies,self.all_sprites)
                elif self.enemy_ghost.is_looking == "izquierda":
                    if self.enemy_ghost.rect.left > self.pingu.rect.right:
                        self.enemy_ghost.shoot_projectile(
                        self.enemy_ghost.rect.x+10,self.enemy_ghost.rect.y+10,self.enemy_ghost.is_looking,self.sprite_projectiles_enemies,self.all_sprites)                    
            else:
                self.enemy_ghost.is_doing = "camina"

        #Wolf
        if self.enemy_wolf.count_life > 0:
            if self.enemy_wolf.see_objective(self.pingu):
                if self.enemy_wolf.is_looking == "derecha":
                    if self.enemy_wolf.rect.right < self.pingu.rect.left:
                        self.enemy_wolf.speed = self.enemy_wolf.speed_buff
                elif self.enemy_wolf.is_looking == "izquierda":    
                    if self.enemy_wolf.rect.left > self.pingu.rect.right:  
                        self.enemy_wolf.speed = self.enemy_wolf.speed_buff                
            else:
                self.enemy_wolf.speed = SPEED_WOLF

        #BOSS:
        if self.boss.count_life > 0:

            self.boss.attack_ice(self.sprite_projectiles_enemies,self.all_sprites)
            self.boss.attack_water(self.sprite_projectiles_enemies,self.all_sprites)
            self.boss.attack_fire(
            self.sprite_projectiles_enemies,self.all_sprites)
            self.boss.dash()



        if self.boss.see_objective(self.pingu):
            self.boss.attack_one_fire(
            self.sprite_projectiles_enemies,self.all_sprites,(self.boss.rect_ojos.x,self.boss.rect_ojos.y))
            

#Items
        for item in self.sprite_items:
            item.buff(self.pingu)


        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        if self.pingu.count_life <= 0:
            time.sleep(1)
            self.show_screen_game_over()
            

        if get_mode():
            self.screen.fill("Blue",self.pingu.rect_pies)

            for platform in self.sprite_platforms:
                self.screen.fill("Green",platform.floor_collision)
            self.screen.fill("Blue",self.enemy_bird.rect)
            self.screen.fill("Red",self.enemy_ghost.rect_ojos)
            self.screen.fill("Red",self.enemy_wolf.rect_ojos)
            self.screen.fill("Blue",self.enemy_wolf.rect_pies)
            self.screen.fill("Red",self.boss.rect_ojos)

        pygame.display.flip()


#---------------------------------------------------------
    def add_sprite(self,element_sprite):

        self.sprites.add(element_sprite)


    def play_music (self,sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()


    def play_sound(self,path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.3)
        sound.play()

    def controller_movement (self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.pingu.is_doing = "izquierda"
            self.pingu.is_looking = "izquierda"

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.pingu.is_doing = "derecha"
            self.pingu.is_looking = "derecha"
        elif keys[pygame.K_x] or keys[pygame.K_k]:
            self.pingu.is_doing = "salta"
        elif keys[pygame.K_j] or keys[pygame.K_z]:
            self.pingu.is_doing = "dispara"              
        else:
            self.pingu.is_doing = "quieto"     

    def create_list_platforms(self):
        #Level 1:
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

        #Level 2:

        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform
    
    def create_platform_boss(self):

        list_platform = []
        #Base
        list_platform.append(self.create_platform((0,HEIGHT-20), (WIDTH,30)))

        #Primeros escalones
        #list_platform.append(self.create_platform((370, HEIGHT-200), SIZE_PLATFORM_BIG))
        #list_platform.append(self.create_platform((0, HEIGHT-300), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-200), SIZE_PLATFORM_SMALL))

        #MEDIO
        list_platform.append(self.create_platform((CENTER_X-310, HEIGHT-400), SIZE_PLATFORM_MEDIUM))
        #list_platform.append(self.create_platform((0, HEIGHT-600), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-400), SIZE_PLATFORM_SMALL))

        #TOP
        #list_platform.append(self.create_platform((CENTER_X-310, HEIGHT-600), SIZE_PLATFORM_MEDIUM))
        #list_platform.append(self.create_platform((0, HEIGHT-600), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-600), SIZE_PLATFORM_SMALL))


        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform
    
    def create_platform(self,position:tuple,size:tuple):
        platform = Platform(rf"assets\items\platforms\ice.png",position,size)
        return platform



    def create_list_platforms_level_2(self):
        #Level 1:
        list_platform = []
        #Base
        list_platform.append(self.create_platform((0,HEIGHT-20), (WIDTH,30)))

        #Primeros escalones
        list_platform.append(self.create_platform((120, HEIGHT-200), SIZE_PLATFORM_GIGANT))
        #list_platform.append(self.create_platform((0, HEIGHT-200), SIZE_PLATFORM_GIGANT))
        #list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-200), SIZE_PLATFORM_SMALL))

        #MEDIO
        list_platform.append(self.create_platform((120, HEIGHT-400), SIZE_PLATFORM_GIGANT))
        #list_platform.append(self.create_platform((0, HEIGHT-400), SIZE_PLATFORM_SMALL))
        #list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_GIGANT[0], HEIGHT-400), SIZE_PLATFORM_GIGANT))

        #TOP
        list_platform.append(self.create_platform((120, HEIGHT-600), SIZE_PLATFORM_GIGANT))
        #list_platform.append(self.create_platform((0, HEIGHT-600), SIZE_PLATFORM_GIGANT))
        #list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-600), SIZE_PLATFORM_SMALL))

        #Level 2:

        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)

        return list_platform


    def create_enemies (self):
        #ENEMIGOS
        # self.enemy_bird = Bird((random.randint(1,WIDTH-10),random.randint(140,800)))
        # self.enemy_ghost = Ghost((random.randint(1,WIDTH-10),random.randint(140,800)))
        # self.enemy_wolf = Wolf ((random.randint(1,WIDTH-10),random.randint(140,800)))
        self.boss = Boss((random.randint(1,WIDTH-300),HEIGHT-300))

        # self.all_sprites.add(self.enemy_bird)
        # self.all_sprites.add(self.enemy_ghost)
        # self.all_sprites.add(self.enemy_wolf)
        self.all_sprites.add(self.boss)   

        # self.sprite_enemies.add(self.enemy_bird)
        # self.sprite_enemies.add(self.enemy_ghost)
        # self.sprite_enemies.add(self.enemy_wolf)
        self.sprite_enemies.add(self.boss)
