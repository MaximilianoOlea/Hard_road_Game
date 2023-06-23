import pygame
from tools import *

#Lista animaciones pingu
# 0 a 3 = quieto derecha
# 4 a 7 = quieto izquierda
# 8 a 14 = camina derecha
# 15 a 21 = camina izquierda
# 22 a 23 = salta derecha
# 24 a 25 = salta izquierda
# 26 a 28 = dispara derecha
# 29 a 31 = dispara izquierda
# 32 = muere derecha
# 33 = muere izquierda
tupla_quieto_derecha = (0,1,2,3)
tupla_quieto_izquierda = (4,5,6,7)
tupla_camina_derecha = (8,9,10,11,12,13,14)
tupla_camina_izquierda = (15,16,17,18,19,20,21)
tupla_salta_derecha = (22,23)
tupla_salta_izquierda = (24,25)
tupla_dispara_derecha = (26,27,28)
tupla_dispara_izquierda = (29,30,31)

pingu_animations= [pygame.image.load(rf"assets\pingu\quieto\0.png"),
                    pygame.image.load(rf"assets\pingu\quieto\1.png"),
                    pygame.image.load(rf"assets\pingu\quieto\2.png"),
                    pygame.image.load(rf"assets\pingu\quieto\3.png"),
                    pygame.image.load(rf"assets\pingu\quieto\left_0.png"),
                    pygame.image.load(rf"assets\pingu\quieto\left_1.png"),
                    pygame.image.load(rf"assets\pingu\quieto\left_2.png"),
                    pygame.image.load(rf"assets\pingu\quieto\left_3.png"), #Quieto
                    pygame.image.load(rf"assets\pingu\camina\0.png"),
                    pygame.image.load(rf"assets\pingu\camina\1.png"),
                    pygame.image.load(rf"assets\pingu\camina\2.png"),
                    pygame.image.load(rf"assets\pingu\camina\3.png"),
                    pygame.image.load(rf"assets\pingu\camina\4.png"),
                    pygame.image.load(rf"assets\pingu\camina\5.png"),
                    pygame.image.load(rf"assets\pingu\camina\6.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_0.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_1.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_2.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_3.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_4.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_5.png"),
                    pygame.image.load(rf"assets\pingu\camina\left_6.png"), #Camina
                    pygame.image.load(rf"assets\pingu\salta\0.png"), 
                    pygame.image.load(rf"assets\pingu\salta\1.png"),
                    pygame.image.load(rf"assets\pingu\salta\left_0.png"),
                    pygame.image.load(rf"assets\pingu\salta\left_1.png"),  #Salta 
                    pygame.image.load(rf"assets\pingu\disparar\0.png"),
                    pygame.image.load(rf"assets\pingu\disparar\1.png"),
                    pygame.image.load(rf"assets\pingu\disparar\2.png"),
                    pygame.image.load(rf"assets\pingu\disparar\left_0.png"),
                    pygame.image.load(rf"assets\pingu\disparar\left_1.png"),
                    pygame.image.load(rf"assets\pingu\disparar\left_2.png"),#dispara
                    pygame.image.load(rf"assets\pingu\Muerte\0.png"),
                    pygame.image.load(rf"assets\pingu\Muerte\left_0.png") #Muere
                    ]


enemy_bird_animations = [pygame.image.load(rf"assets\enemies\bird\0.png"),
                    pygame.image.load(rf"assets\enemies\bird\1.png"),
                    pygame.image.load(rf"assets\enemies\bird\2.png"),
                    pygame.image.load(rf"assets\enemies\bird\left_0.png"),
                    pygame.image.load(rf"assets\enemies\bird\left_1.png"),
                    pygame.image.load(rf"assets\enemies\bird\left_2.png"),]

tupla_enemy_bird_derecha = (0,1,2)
tupla_enemy_bird_izquierda = (3,4,5)

