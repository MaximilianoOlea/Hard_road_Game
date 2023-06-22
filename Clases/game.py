import pygame

import sys 

from Configuraciones.config_assets import *

from Configuraciones.mode import *

from Configuraciones.diccionarios_assets import *

from Configuraciones.charge_list_animations import *

from .pingu import Pingu


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

        #Piso
        self.piso = pygame.Rect(600,0,500,20)
        self.piso.top = self.pingu.rect.bottom + 300
        self.piso_sides = get_rectangles(self.piso)

        self.piso2 = pygame.Rect(600,0,500,20)
        self.piso2.top = 500


        self.piso3 =  pygame.Rect(600,0,500,20)
        self.piso3.top = 300

        self.piso4 = pygame.Rect(600,0,500,20)
        self.piso4.top = 200

        self.lista_pisos = []
        self.lista_pisos.append(self.piso4)
        self.lista_pisos.append(self.piso2)
        self.lista_pisos.append(self.piso3)
        self.index_piso = 0

        bubble_sort_pisos(self.lista_pisos)

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
        self.finalizado = True
        self.show_screen_game_over()

# -------------------

    def reset(self):  # Debe recibir el nivel
        pass

    # Muestra la pantalla de partida perdida
    def show_screen_game_over(self, image):
        pass

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
                    if not self.pause:
                        self.pingu.is_doing = "dispara"              
                        print ("dispara")
                elif evento.key == pygame.K_DOWN:
                    if self.pingu.is_in_floor:
                        self.pingu.bajar_plataforma = True
                        self.pingu.is_in_floor = False

        

        if not self.pause:
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

        # self.pingu.update()
        #self.pingu.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        # for piso in self.lista_pisos:
        #     if not self.pingu.is_in_floor:
        #         self.pingu.check_collision_floor(piso)
        #         print("----------------------------------------")
        #         print ("Esta en el piso",self.pingu.is_in_floor)
        #         print ("Bajar de plataforma",self.pingu.bajar_plataforma)
        #         print ("Esta saltando",self.pingu.is_jumping)
        #         print("----------------------------------------")
        #     print("*****************************************")
        #     print ("Esta en el piso",self.pingu.is_in_floor)
        #     print ("Bajar de plataforma",self.pingu.bajar_plataforma)
        #     print ("Esta saltando",self.pingu.is_jumping)
        #     print("*****************************************")


        for i in range(len(self.lista_pisos)):
            if not self.pingu.is_in_floor:
                self.pingu.check_collision_floor(self.lista_pisos[i])

        if get_mode():
            for lado in self.piso_sides:
                pygame.draw.rect(self.screen,"Yellow",self.piso_sides[lado],3)
            self.screen.fill("Yellow",self.lista_pisos[0])
            self.screen.fill("Red",self.lista_pisos[1])
            self.screen.fill("Green",self.lista_pisos[2])
            self.screen.fill("Blue",self.pingu.rect_pies)

        pygame.display.flip()


#---------------------------------------------------------
    def add_sprite(self,element_sprite):

        self.sprites.add(element_sprite)


    def play_sound (self,sound):
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

    def play_music (self,sound):
        pygame.mixer.init
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(-1)

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
