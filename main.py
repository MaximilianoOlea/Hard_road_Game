import pygame

from Clases.game import Game

from Configuraciones.config_assets import *


mi_juego  = Game (SIZE_SCREEN,"Hard climber","assets\items\pingu_proyectile.png")
mi_juego.start(FPS)