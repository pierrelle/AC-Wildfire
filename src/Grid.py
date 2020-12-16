import random
from typing import Tuple

import numpy as np
import pygame
import pygame.draw
from pygame import Rect
from pygame.event import Event

from .Parameters import Parameters


class Grid(object):
    _grid = None
    _index_neighbors = [
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, 2), (2, 0)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, -2), (0, 2)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (-2, 0), (0, -2), (2, 0)],
        [(-1, 0), (0, -1), (0, 1), (1, 0), (0, -2), (0, 2), (2, 0)],
    ]

    def __init__(self, grid_dim: Tuple, parameters: Parameters):
        self.GRID_DIM = grid_dim
        self._density1 = parameters.density1
        self._density2 = parameters.density2
        self._wind = parameters.wind

        self._grid = np.zeros(self.GRID_DIM, dtype="int8")
        for x in range(self.GRID_DIM[0]):
            for y in range(self.GRID_DIM[1]):
                n = random.randint(1, 101)
                if n < self._density1 * 100:
                    self._grid[x, y] = 1
                elif n < (self._density1 + self._density2) * 100:
                    self._grid[x, y] = 2

        if parameters.firebreak:
            for x in range(
                self.GRID_DIM[0] // 4, self.GRID_DIM[0], (self.GRID_DIM[0] // 4)
            ):
                for y in range(self.GRID_DIM[1]):
                    self._grid[x, y] = 0
            for y in range(
                self.GRID_DIM[0] // 4, self.GRID_DIM[1], (self.GRID_DIM[1] // 4)
            ):
                for x in range(self.GRID_DIM[0]):
                    self._grid[x, y] = 0

    def _get_index_neighbors(self, x: int, y: int):
        """Return the range index of the fire for neighbores cells.
        1 for simple range, 2 for double range, when the wind push
        the fire in a specific direction.

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.

        Returns:
            [List[Tuple]]: [description]
        """
        return [
            (dx + x, dy + y)
            for (dx, dy) in self._index_neighbors[self._wind.value]
            if dx + x >= 0
            and dx + x < self.GRID_DIM[0]
            and dy + y >= 0
            and dy + y < self.GRID_DIM[1]
        ]

    def get_neighbors(self, x: int, y: int):
        """[summary]

        Args:
            x (int): X coordinate of the cell.
            y (int): Y coordinate of the cell.

        Returns:
            [List[int]]]: [description]
        """
        return [self._grid[vx, vy] for (vx, vy) in self._get_index_neighbors(x, y)]
