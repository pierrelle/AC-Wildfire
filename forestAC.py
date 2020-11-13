import sys, math, random
import pygame
from pygame import Rect
import pygame.draw
from pygame.event import Event
import numpy as np
from enum import Enum

# TODO: Voir si on ajoute la distance dans les proba, si oui comment
# TODO: Voir si on fait des compositions de terrains différentes, si oui lesquelles
# TODO: Voir si on fait des graphes pour visualiser la percolation en fonction des valeurs
# TODO: Cleaner ce bordel de code, voir quelle norme on prend 


class Wind(Enum):
    South = 0
    West = 1
    North = 2
    East = 3


__screenSize__ = (600, 600)  # (900,900) (1280,1280)
__cellSize__ = 10
__gridDim__ = tuple(map(lambda x: int(x / __cellSize__), __screenSize__))
__colors__ = [(255, 255, 255), (26, 174, 70), (7, 70, 22), (194, 46, 28), (107, 30, 30)]
__refreshTime__ = 10000


# The sum of densities must be included between 0 and 1
__density1__ = 0.4
__density2__ = 0.1
__nbInitialFires__ = 3
__wind__ = Wind.West  # South, West, North, East

__resistanceTree1__ = 1
__resistanceTree2__ = 1.3
__transmissibilityFire1__ = 0.3
__transmissibilityFire2__ = 0.5


def getColorCell(n):
    return __colors__[n]


class Grid:
    _grid = None
    _indexVoisins = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    _indexVoisinsWind = [
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, 2), (2, 0)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, -2), (0, 2)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, -2), (2, 0)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (0, -2), (0, 2), (2, 0)],
    ]

    def __init__(self, parameters):
        print("Creating a grid of dimensions " + str(__gridDim__))
        self._density1 = parameters.__density1__
        self._density2 = parameters.__density2__
        self._wind = parameters.__wind__

        self._grid = np.zeros(__gridDim__, dtype="int8")
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                n = random.randint(1, 101)
                if n < self._density1 * 100:
                    self._grid[x, y] = 1
                elif n < (self._density1 + self._density2) * 100:
                    self._grid[x, y] = 2

    def indiceVoisins(self, x, y):
        return [
            (dx + x, dy + y)
            for (dx, dy) in self._indexVoisins
            if dx + x >= 0
            and dx + x < __gridDim__[0]
            and dy + y >= 0
            and dy + y < __gridDim__[1]
        ]

    def indiceVoisinsWind(self, x, y):
        return [
            (dx + x, dy + y)
            for (dx, dy) in self._indexVoisinsWind[self._wind.value]
            if dx + x >= 0
            and dx + x < __gridDim__[0]
            and dy + y >= 0
            and dy + y < __gridDim__[1]
        ]

    def voisins(self, x, y):
        return [self._grid[vx, vy] for (vx, vy) in self.indiceVoisinsWind(x, y)]

    def drawMe(self):
        pass


class Scene:
    class Parameters:
        def __init__(self):
            self.__density1__ = __density1__
            self.__density2__ = __density2__
            self.__nbInitialFires__ = __nbInitialFires__
            self.__wind__ = __wind__

        def randomize(self):
            rnd = random.Random()
            randomWind = rnd.randint(0, 3)
            print(randomWind)
            self.__wind__ = Wind(randomWind)
            randomFires = rnd.randint(1, 10)
            self.__nbInitialFires__ = randomFires
            randomTree = rnd.uniform(0.3, 0.8)
            self.__density1__ = randomTree
            randomTree2 = rnd.uniform(0, 0.2)
            self.__density2__ = randomTree2

    _mouseCoords = (0, 0)
    _grid = None
    _font = None

    def __init__(self, random=False):
        pygame.init()
        pygame.display.set_caption("Forest Cellular Automaton")
        self._screen = pygame.display.set_mode(
            (__screenSize__[0], __screenSize__[1] + 110)
        )
        self._font = pygame.font.SysFont("Monospace", 18, bold=True)
        self._parameters = self.Parameters()
        if random:
            self._parameters.randomize()
        self._grid = Grid(self._parameters)

    def drawMe(self):
        if self._grid._grid is None:
            return
        self._screen.fill((255, 255, 255))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(
                    self._screen,
                    getColorCell(self._grid._grid.item((x, y))),
                    (
                        x * __cellSize__ + 1,
                        y * __cellSize__ + 1,
                        __cellSize__ - 2,
                        __cellSize__ - 2,
                    ),
                )

    def displayText(self):
        topPadding = 8
        windText = f"Wind : {self._parameters.__wind__.name}"
        fireText = f"Initial fires : {self._parameters.__nbInitialFires__}"
        density1Text = f"Density light Tree : {round(self._parameters.__density1__, 2)}"
        density2Text = f"Density heavy Tree : {round(self._parameters.__density2__, 2)}"
        labels = [windText, fireText, density1Text, density2Text]
        for lab in labels:
            rect = Rect(10, __screenSize__[1] + topPadding, 200, 100)
            topPadding += 25
            self.drawText(lab, rect)

    def drawText(self, text, position, color=(0, 0, 0)):
        self._screen.blit(self._font.render(text, 1, color), position)

    def initiate_fire(self):
        nb_fire = self._parameters.__nbInitialFires__
        while nb_fire != 0:
            x = random.randint(0, __gridDim__[0] - 1)
            y = random.randint(0, __gridDim__[1] - 1)
            if self._grid._grid[x, y] == 1:
                self._grid._grid[x, y] = 3
                nb_fire -= 1
        
    def _calculate_probability(self,x,y):
        resistanceTree = __resistanceTree1__
        if self._grid._grid[x, y] == 2:
            resistanceTree = __resistanceTree2__
        voisins = self._grid.voisins(x, y)

        [nbFire1, nbFire2, nbFireDistance1, nbFireDistance2] = [0,0,0,0]
        for tree in voisins:
            if tree == 3:
                nbFire1 += 1
            if tree == 4:
                nbFire2 += 1

        res = (nbFire1 * __transmissibilityFire1__ + nbFire2 * __transmissibilityFire2__)/resistanceTree
        res = min(res,1)
        return res
        

    def update(self):
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                proba = 0
                # Count how many neighbour trees are on fire
                if self._grid._grid[x, y] == 1 or self._grid._grid[x, y] == 2:
                    proba = self._calculate_probability(x,y)

                # If conditions are satisfied, prepare the tree to be on fire
                index = random.randint(1,100)
                if index <= proba*100 :
                    self._grid._grid[x, y] = 5


        # Update the value of each tree, to put them on fire or stop the fire
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                if self._grid._grid[x, y] == 4:
                    self._grid._grid[x, y] = 0
                if self._grid._grid[x, y] == 3:
                    self._grid._grid[x, y] = 4
                if self._grid._grid[x, y] == 5:
                    self._grid._grid[x, y] = 3

    def eventClic(self, coord, b):
        pass

    def recordMouseMove(self, coord):
        pass


def main():
    done = False
    refresh = True
    while done == False:
        if refresh == True:
            scene = Scene(random=True)
            scene.initiate_fire()
            timer = pygame.time.set_timer(32774, __refreshTime__)
            refresh = False
        clock = pygame.time.Clock()
        scene.drawMe()
        scene.displayText()
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
