import pygame

import sys 

from Configuraciones.config_assets import *

from Configuraciones.mode import *

from Configuraciones.diccionarios_assets import *

from Configuraciones.charge_list_animations import *

from .pingu import Pingu

from .platform import Platform

from .enemy import *

def bubble_sort_pisos(lista_pisos):
    n = len(lista_pisos)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lista_pisos[j].y < lista_pisos[j + 1].y:
                lista_pisos[j], lista_pisos[j + 1] = lista_pisos[j + 1], lista_pisos[j]

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
        self.background = pygame.image.load("assets\\backgrounds\grass.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        #Sprites
        self.all_sprites = pygame.sprite.Group()

        self.pingu = Pingu((main_character_x,main_character_y))
        self.all_sprites.add(self.pingu)

        self.sprite_platforms = pygame.sprite.Group()
        self.sprite_projectiles = pygame.sprite.Group()


        self.sprite_enemies = pygame.sprite.Group()
        self.enemy_bird = Bird((10,40))
        self.all_sprites.add(self.enemy_bird)
        self.sprite_enemies.add(self.enemy_bird)
        self.create_list_platforms()


        self.fuente = pygame.font.Font(rf"assets\fonts\gameplay.ttf",48)

        pygame.mixer.init()
        pygame.mixer.music.load(rf"assets\sounds\menu\gameover_trap.mp3")
# ------------------------------------------------------

        # bubble_sort_pisos(self.lista_pisos)

        # self.plataforma = Platform(rf"assets\items\platforms\earth.png",CENTER,SIZE_PLATFORM_MEDIUM)
        # self.sprite_platforms = pygame.sprite.Group()

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
        self.jugando = False
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

        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        for platform in self.sprite_platforms:
            self.pingu.check_collision_floor(platform.floor_collision)
        
        # for projectile in self.sprite_projectiles:
        #     for enemy in self.sprite_enemies:
        #         if enemy.count_life < 0:
        #             lista = pygame.sprite.spritecollide(projectile, enemy, True)
        #         else:
        #             lista = pygame.sprite.spritecollide(projectile, enemy, False)
        #             enemy.count_life -= 1

        #     if len(lista):
        #         projectile.kill()

        for projectile in self.sprite_projectiles:
            for enemy in self.sprite_enemies:
                if projectile.check_objective(enemy):
                    if enemy.count_life < 0:
                        enemy.kill()

        self.pingu.dead(self.enemy_bird)
        print (self.pingu.is_alive)
        print (self.pingu.count_life)

        if self.pingu.count_life <= 0:
            time.sleep(1)
            self.show_screen_game_over()
            

        if get_mode():
            self.screen.fill("Blue",self.pingu.rect_pies)

            for platform in self.sprite_platforms:
                self.screen.fill("Green",platform.floor_collision)

        pygame.display.flip()


#---------------------------------------------------------
    def add_sprite(self,element_sprite):

        self.sprites.add(element_sprite)


    def play_sound (self,sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()


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
        list_platform.append(self.create_platform((CENTER_X-350, HEIGHT-400), SIZE_PLATFORM_MEDIUM))
        list_platform.append(self.create_platform((0, HEIGHT-400), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-400), SIZE_PLATFORM_SMALL))

        #TOP
        list_platform.append(self.create_platform((CENTER_X-350, HEIGHT-600), SIZE_PLATFORM_MEDIUM))
        list_platform.append(self.create_platform((0, HEIGHT-600), SIZE_PLATFORM_SMALL))
        list_platform.append(self.create_platform((WIDTH - SIZE_PLATFORM_SMALL[0], HEIGHT-600), SIZE_PLATFORM_SMALL))

        #Level 2:



        for platform in list_platform:
            self.all_sprites.add(platform)
            self.sprite_platforms.add(platform)
    def create_platform(self,position:tuple,size:tuple):
        platform = Platform(rf"assets\items\platforms\earth.png",position,size)
        return platform