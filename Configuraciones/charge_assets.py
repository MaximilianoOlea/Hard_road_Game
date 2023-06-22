import pygame
from tools import *


#Pingu (Personaje principal)
# pingu_still= [pygame.image.load(rf"assets\pingu\quieto\0.png"),
#                     pygame.image.load(rf"assets\pingu\quieto\1.png"),
#                     pygame.image.load(rf"assets\pingu\quieto\2.png"),
#                     pygame.image.load(rf"assets\pingu\quieto\3.png"),
#                     pygame.image.load(rf"assets\pingu\quieto\4.png"),]

# pingu_still_left= turn_images(pingu_still,True,False)

# pingu_walk =  [pygame.image.load(rf"assets\pingu\camina\0.png"),
#                     pygame.image.load(rf"assets\pingu\camina\1.png"),
#                     pygame.image.load(rf"assets\pingu\camina\2.png"),
#                     pygame.image.load(rf"assets\pingu\camina\3.png"),
#                     pygame.image.load(rf"assets\pingu\camina\4.png"),
#                     pygame.image.load(rf"assets\pingu\camina\5.png"),
#                     pygame.image.load(rf"assets\pingu\camina\6.png"),
#                     pygame.image.load(rf"assets\pingu\camina\7.png")]

# pingu_walk_left = turn_images(pingu_walk,True,False)

# pingu_jump = [pygame.image.load(rf"assets\pingu\salta\\1.png"),  
#             pygame.image.load(rf"assets\pingu\salta\\2.png"),
#             pygame.image.load(rf"assets\pingu\salta\\3.png")]

# pingu_jump_left = turn_images(pingu_jump,True,False)

# pingu_died = [pygame.image.load(rf"assets\pingu\Muerte\0.png")]
# pingu_died_left = turn_images(pingu_died,True,False)

# pingu_shooting = [pygame.image.load(rf"assets\pingu\disparar\\0.png"),
#                 pygame.image.load(rf"assets\pingu\disparar\\1.png"), 
#                 pygame.image.load(rf"assets\pingu\disparar\\2.png")]
# pingu_shooting_left = turn_images(pingu_shooting,True,False)

#Enemigos:
enemy_bird = [pygame.image.load(rf"assets\enemies\\bird\\0.png"),
            pygame.image.load(rf"assets\enemies\\bird\\1.png"),
            pygame.image.load(rf"assets\enemies\\bird\\2.png")]

enemy_bird_left  = turn_images(enemy_bird,True,False)


enemy_wolf = [pygame.image.load("assets\enemies\wolf\camina\\0.png"),
            pygame.image.load("assets\enemies\wolf\camina\\1.png"),
            pygame.image.load("assets\enemies\wolf\camina\\2.png"),
            pygame.image.load("assets\enemies\wolf\camina\\3.png"),
            pygame.image.load("assets\enemies\wolf\camina\\4.png"),
            pygame.image.load("assets\enemies\wolf\camina\\5.png"),
            pygame.image.load("assets\enemies\wolf\camina\\6.png"),
            pygame.image.load("assets\enemies\wolf\camina\\7.png"),
            pygame.image.load("assets\enemies\wolf\camina\\8.png"),
            pygame.image.load("assets\enemies\wolf\camina\\9.png"),
            pygame.image.load("assets\enemies\wolf\camina\\10.png"),
            pygame.image.load("assets\enemies\wolf\camina\\11.png")]

enemy_wolf_left = turn_images(enemy_wolf,True,False)
enemy_wolf_died = [pygame.image.load("assets\enemies\wolf\muerte\\12.png"),
                pygame.image.load("assets\enemies\wolf\muerte\\13.png")]

enemy_wolf_died_left = turn_images(enemy_wolf_died,True,False)

enemy_ghost = [pygame.image.load("assets\enemies\ghost\camina\\0.png"),
            pygame.image.load("assets\enemies\ghost\camina\\1.png"),
            pygame.image.load("assets\enemies\ghost\camina\\2.png"),
            pygame.image.load("assets\enemies\ghost\camina\\3.png"),]

enemy_ghost_left = turn_images(enemy_ghost,True,False)

enemy_ghost_shoot = [pygame.image.load("assets\enemies\ghost\dispara\\4.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\5.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\6.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\7.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\8.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\9.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\10.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\11.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\12.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\13.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\14.png"),
                pygame.image.load("assets\enemies\ghost\dispara\\15.png")]

enemy_ghost_shoot = turn_images(enemy_ghost_shoot,True,False)

enemy_ghost_died = [pygame.image.load("assets\enemies\ghost\muerte\\4.png"),
                pygame.image.load("assets\enemies\ghost\muerte\\5.png")]

enemy_ghost_died_left = turn_images(enemy_ghost_died,True,False)

#Bosses:
boss_fire = [pygame.image.load("assets\enemies\\boss\\fireboss\\0.png"),
            pygame.image.load("assets\enemies\\boss\\fireboss\\1.png")]
boss_fire_left = turn_images(boss_fire,True,False)

boss_ice = [pygame.image.load("assets\enemies\\boss\\iceboss\\0.png"),
            pygame.image.load("assets\enemies\\boss\\iceboss\\1.png")]
boss_ice_left = turn_images(boss_ice,True,False)

boss_water = [pygame.image.load("assets\enemies\\boss\\waterboss\\0.png"),
            pygame.image.load("assets\enemies\\boss\\waterboss\\1.png")]
boss_water_left = turn_images(boss_water,True,False)

#Proyectiles:
projectile_fire = [pygame.image.load("assets\enemies\\boss\\fireboss\power\enemigo_fantasma_proyectil.png")]
projectile_fire_left = turn_images(projectile_fire,True,False)
projectile_ice= [pygame.image.load("assets\enemies\\boss\iceboss\powers\projectile_ice.png")]
projectile_ice_left = turn_images(projectile_ice,True,False)
projectile_water = [pygame.image.load("assets\enemies\\boss\waterboss\power\\1.png"),
                pygame.image.load("assets\enemies\\boss\waterboss\power\\2.png")]
projectile_water_left = turn_images(projectile_water,True,False)
projectile_pingu = [pygame.image.load(rf"assets\items\pingu_proyectile.png")]
projectile_pingu_left = turn_images(projectile_water,True,False)

#Climas:
climate_rain = [pygame.image.load("assets\\backgrounds\\rain\\rain_drops-01.png"),
            pygame.image.load("assets\\backgrounds\\rain\\rain_drops-02.png"),
            pygame.image.load("assets\\backgrounds\\rain\\rain_drops-03.png"),
            pygame.image.load("assets\\backgrounds\\rain\\rain_drops-04.png")]

climate_rain_left  = turn_images(climate_rain,True,False)

climate_wind = [pygame.image.load("assets\\backgrounds\wind\Leaves1.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves2.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves3.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves4.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves5.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves6.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves7.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves8.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves9.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves10.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves11.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves12.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves13.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves14.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves15.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves16.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves17.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves18.png"),
            pygame.image.load("assets\\backgrounds\wind\Leaves19.png")]

climate_wind_left = turn_images(climate_wind,True,False)