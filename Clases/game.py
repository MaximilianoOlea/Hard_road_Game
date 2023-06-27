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

from .levels import *

from .menu import Menu

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
        self.menu = Menu()
#LEVELs
        self.index_level = 0
        self.list_levels = [Level1(),Level2(),Level3()]

        pygame.mixer.init()
        pygame.mixer.music.load(self.list_levels[self.index_level].music)
        pygame.mixer.music.play(-1)
        
        self.pingu = Pingu((main_character_x,main_character_y))
        self.list_levels[self.index_level].all_sprites.add(self.pingu)

        self.game_over_music = False
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
        self.pause = False
        while self.playing:
            self.clock.tick(fps)
            self.handle_event()


        
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

    def win_level (self):

        if not self.list_levels[self.index_level].sprite_enemies:
            self.list_levels[self.index_level].all_sprites.remove(self.pingu)
            self.index_level += 1
            if self.index_level < len(self.list_levels):
                self.list_levels[self.index_level].all_sprites.add(self.pingu)
                self.pingu.rect.x = self.pingu.pos_respaw[0]
                self.pingu.rect.y = self.pingu.pos_respaw[1]
                self.pingu.rect_pies.x = self.pingu.pos_respaw[0]
                self.pingu.rect_pies.y = self.pingu.rect.bottom 
                self.change_music()
            else:
                self.play_music(rf"assets\sounds\menu\gameover_trap.mp3")
                print("No hay mas niveles")

    def change_music(self):
        pygame.mixer.music.stop()
        self.play_sound(rf"assets\sounds\menu\win.mp3")
        time.sleep(2)
        if self.index_level < len(self.list_levels):
            pygame.mixer.music.load(self.list_levels[self.index_level].music)  # Carga la música del siguiente nivel
            pygame.mixer.music.play(-1)



# -------------------

    def reset(self):  # Debe recibir el nivel
        pass

    # Muestra la pantalla de partida perdida
    def show_screen_game_over(self):
        if not self.game_over_music:
            pygame.mixer.music.stop()  
            pygame.mixer.music.load(rf"assets\sounds\menu\gameover_trap.mp3")  
            pygame.mixer.music.play(-1) 
            self.game_over_music = True

        texto = self.list_levels[0].fuente.render("Game Over", True, (0, 0, 255))
        rect_texto = texto.get_rect()
        rect_texto.center = CENTER
        self.screen.fill((0, 0, 0))
        self.screen.blit(texto, rect_texto)
        pygame.display.flip()

        pygame.display.flip()


    def draw_score(self,score):

        texto = self.list_levels[0].fuente.render(f"Score:{score}",True,(ROJO))
        rect_texto = texto.get_rect()
        rect_texto.x = 10
        self.screen.blit(texto,rect_texto)

    def draw_life(self,count_life):
        icon_vida = pygame.image.load(rf"assets\menu\life.png")
        icon_vida = pygame.transform.scale(icon_vida, (40,60)) 
        rect_icon_vida = icon_vida.get_rect()
        rect_icon_vida.x = WIDTH-150
        self.screen.blit(icon_vida,rect_icon_vida)
        texto = self.list_levels[0].fuente.render(f"{count_life}",True,(AZUL))
        rect_texto = texto.get_rect()
        rect_texto.x = rect_icon_vida.x + 60
        self.screen.blit(texto,rect_texto)

    def show_screen_pause(self):
        # Pausa el juego,muestra Opcion de Reinicio | volver al juego |Salir al menu principal
        self.pause = not self.pause
        self.play_sound(rf"assets\sounds\menu\pause.mp3")

        if self.pause:
            pygame.mixer.music.pause()  # Pausa la música
        else:
            pygame.mixer.music.unpause()  # Reanuda la música

        return self.pause
    
#Manejador de eventos:
    def handle_event(self):
        """_summary_
        Controla los eventos del juego
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.exit()
            elif evento.type == pygame.KEYDOWN :

                if self.index_level < len(self.list_levels):
                    if evento.key == pygame.K_TAB:
                        change_mode()  # Modo admid (Ver rectangulos de colision)
                    elif evento.key == pygame.K_RETURN:
                        self.show_screen_pause()
                    elif evento.key == pygame.K_j or evento.key == pygame.K_z:
                        if not self.pause and self.pingu.is_alive:
                            self.pingu.is_doing = "dispara"              
                            self.pingu.shoot_projectile_pingu(
                            self.pingu.rect.x,self.pingu.rect.y,
                            self.pingu.is_looking,self.list_levels[self.index_level].sprite_projectiles,self.list_levels[self.index_level].all_sprites)

                    elif evento.key == pygame.K_DOWN:
                        if self.pingu.is_in_floor:
                            self.pingu.bajar_plataforma = True
                            self.pingu.is_in_floor = False
                    elif evento.key == pygame.K_p: #Agregar vida
                        if self.pingu.count_life < 99:
                            self.pingu.count_life+=1
                            self.play_sound(rf"assets\sounds\menu\life.mp3")


        if not self.pause:
            if self.index_level < len(self.list_levels):
                if self.pingu.is_alive:
                    self.controller_movement()
            self.render_screen()
        else: #Display Menu
            self.menu.draw_text("Pausa","Red",self.screen,(750,400))
            pygame.display.flip()

            #Si cae sobre un enemigo
#------------------------------------------------------

    def render_screen(self):#Object_game seran una lista
        """_summary_
        Actualiza los elementos de la pantalla

        Args:
            screen (_type_): Pantalla en la que va a blitearse
            object_game (list): Todos los elementos del juego (Lista de diccionarios)
        """
        if self.index_level < len(self.list_levels):
            self.screen.blit(self.list_levels[self.index_level].background,(ORIGIN))  
            self.draw_score(self.pingu.score)
            self.draw_life(self.pingu.count_life)

            self.pingu.check_collision_floor(self.list_levels[self.index_level].list_platforms)


    #Impacto de disparo hacia un enemigo:
            for enemy in self.list_levels[self.index_level].sprite_enemies:
                for projectile in self.list_levels[self.index_level].sprite_projectiles:
                    if projectile.check_objective(enemy):
                        self.pingu.score += 100
                if enemy.count_life <= 0:
                    enemy.kill()
                    self.list_levels[self.index_level].all_sprites.remove(enemy)
                    self.list_levels[self.index_level].sprite_enemies.remove(enemy)
                    enemy.drop_item(self.list_levels[self.index_level].sprite_items,self.list_levels[self.index_level].all_sprites)

            for projectile in self.list_levels[self.index_level].sprite_projectiles_enemies:
                if projectile.impacted:
                    enemy.drop_item(self.list_levels[self.index_level].sprite_items,self.list_levels[self.index_level].all_sprites)

    #Impacto con enemigo (muerte)

            for enemy in self.list_levels[self.index_level].sprite_enemies:
                self.pingu.dead(enemy)
            for projectile_enemy in self.list_levels[self.index_level].sprite_projectiles_enemies:
                self.pingu.dead(projectile_enemy)    

            #Ghost:

            if self.list_levels[self.index_level].sprite_enemies_ghost:
                for ghost in self.list_levels[self.index_level].sprite_enemies_ghost:
                    if ghost.count_life > 0:
                        if ghost.see_objective(self.pingu):
                            if ghost.is_looking == "derecha":
                                if ghost.rect.right < self.pingu.rect.left:
                                    ghost.shoot_projectile(
                                    ghost.rect.x+10,ghost.rect.y+10,ghost.is_looking,
                                    self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites)
                            elif ghost.is_looking == "izquierda":
                                if ghost.rect.left > self.pingu.rect.right:
                                    ghost.shoot_projectile(
                                    ghost.rect.x+10,ghost.rect.y+10,
                                    ghost.is_looking,self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites)                    
                        else:
                            ghost.is_doing = "camina"

            #Wolf

            for wolf in self.list_levels[self.index_level].sprite_enemies_wolf:
                wolf.check_collision_floor(self.list_levels[self.index_level].list_platforms)

                if wolf.count_life > 0:
                    if wolf.see_objective(self.pingu):
                        if wolf.is_looking == "derecha":
                            if wolf.rect.right < self.pingu.rect.left:
                                wolf.speed = wolf.speed_buff
                        elif wolf.is_looking == "izquierda":    
                            if wolf.rect.left > self.pingu.rect.right:  
                                wolf.speed = wolf.speed_buff                
                    else:
                        wolf.speed = SPEED_WOLF

    #BOSS     
            if self.list_levels[self.index_level].have_boss and self.list_levels[self.index_level].boss.count_life > 0:

                self.list_levels[self.index_level].boss.attack_ice(self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites)
                self.list_levels[self.index_level].boss.attack_water(self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites)
                self.list_levels[self.index_level].boss.attack_fire(
                self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites)
                self.list_levels[self.index_level].boss.dash()

                if self.list_levels[self.index_level].boss.see_objective(self.pingu):
                    self.list_levels[self.index_level].boss.attack_one_fire(
                    self.list_levels[self.index_level].sprite_projectiles_enemies,self.list_levels[self.index_level].all_sprites,
                    (self.list_levels[self.index_level].boss.rect_ojos.x,self.list_levels[self.index_level].boss.rect_ojos.y))
    
    #Item

            for item in self.list_levels[self.index_level].sprite_items:
                item.buff(self.pingu)

            self.list_levels[self.index_level].all_sprites.update()
            self.list_levels[self.index_level].all_sprites.draw(self.screen)

            if self.pingu.count_life <= 0 or self.index_level > len(self.list_levels):
                time.sleep(1)
                self.show_screen_game_over()
                

            if get_mode():
                self.screen.fill("Blue",self.pingu.rect_pies)

                for platform in self.list_levels[self.index_level].sprite_platforms:
                    self.screen.fill("Yellow",platform.floor_collision)

                if self.list_levels[self.index_level].sprite_enemies:
                    for enemy in self.list_levels[self.index_level].sprite_enemies:
                        self.screen.fill ("Red",enemy.rect_pies)
                        self.screen.fill("Green",enemy.rect_ojos)

            self.win_level()
            pygame.display.flip()
        else:
            self.show_screen_game_over()

#---------------------------------------------------------
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
