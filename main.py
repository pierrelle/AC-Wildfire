import sys

import numpy as np
import pygame
import pygame.draw
from pygame import Rect
from pygame.event import Event

from src.Grid import Grid
from src.Parameters import Parameters
from src.Scene import Scene
from src.Wind import Wind

CELL_SIZE = 10
SCREEN_SIZE = (600, 600)  # (900,900) (1280,1280)
GRID_DIM = tuple(map(lambda x: int(x / CELL_SIZE), SCREEN_SIZE))
REFRESH_TIME = 10000
COLORS = [(255, 255, 255), (26, 174, 70), (7, 70, 22), (194, 46, 28), (107, 30, 30)]


parameters = Parameters(
    density1=0.4,  # The sum of densities must be included between 0 and 1
    density2=0.1,
    nbInitialFires=3,
    wind=Wind.West,  # South, West, North, East
    firebreak=True,
    resistanceTree1=1,
    resistanceTree2=1.3,
    transmissibilityFire3=0.3,
    transmissibilityFire4=0.5,
)


def main():
    done = False
    refresh = True
    while done == False:
        if refresh == True:
            scene = Scene(
                SCREEN_SIZE, CELL_SIZE, COLORS, GRID_DIM, parameters, random=True
            )
            scene.initiate_fire()
            pygame.time.set_timer(32774, REFRESH_TIME)
            refresh = False
        clock = pygame.time.Clock()
        scene.draw_me()
        scene.display_text()
        pygame.display.flip()
        scene.update()
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("> Exiting")
                done = True
            if event.type == pygame.USEREVENT or event.type == pygame.MOUSEBUTTONUP:
                print("> Refreshing")
                refresh = True
    pygame.quit()


if not sys.flags.interactive:
    main()
