import random
from typing import List, Tuple

import numpy as np
import pygame
import pygame.draw
from pygame import Rect
from pygame.event import Event

from .Grid import Grid
from .Parameters import Parameters


class Scene(object):
    _grid = None
    _font = None

    def __init__(
        self,
        screen_size: Tuple,
        cell_size: int,
        colors: List,
        grid_dim: Tuple,
        parameters: Parameters,
        random: bool = False,
    ):
        self.SCREEN_SIZE = screen_size
        self.CELL_SIZE = cell_size
        self.COLORS = colors
        self.GRID_DIM = grid_dim
        pygame.init()
        pygame.display.set_caption("Forest Cellular Automaton")
        self._screen = pygame.display.set_mode(
            (self.SCREEN_SIZE[0], self.SCREEN_SIZE[1] + 140)
        )
        self._font = pygame.font.SysFont("Monospace", 18, bold=True)
        self._parameters = parameters
        if random:
            self._parameters.randomize()
        self._grid = Grid(self.GRID_DIM, self._parameters)

    def draw_me(self):
        """Draw the scene"""
        if self._grid._grid is None:
            return
        self._screen.fill((255, 255, 255))
        for x in range(self.GRID_DIM[0]):
            for y in range(self.GRID_DIM[1]):
                pygame.draw.rect(
                    self._screen,
                    self.COLORS[self._grid._grid.item((x, y))],
                    (
                        x * self.CELL_SIZE + 1,
                        y * self.CELL_SIZE + 1,
                        self.CELL_SIZE - 2,
                        self.CELL_SIZE - 2,
                    ),
                )

    def display_text(self):
        """Display information about the generation at the bottom of the screen."""
        top_padding = 8
        wind_text = f"Wind : {self._parameters.wind.name}"
        fire_text = f"Initial fires : {self._parameters.nb_initial_fires}"
        density1_text = f"Density light Tree : {round(self._parameters.density1, 2)}"
        density2_text = f"Density heavy Tree : {round(self._parameters.density2, 2)}"
        firebreak_text = f"Firebreak : {self._parameters.firebreak}"
        labels = [wind_text, fire_text, density1_text, density2_text, firebreak_text]
        for lab in labels:
            rect = Rect(10, self.SCREEN_SIZE[1] + top_padding, 200, 100)
            top_padding += 25
            self.draw_text(lab, rect)

    def draw_text(self, text: str, position: Rect, color: Tuple = (0, 0, 0)):
        """Draw text in a given color and at a specific position.

        Args:
            text (str): Text to draw
            position (Rect): Position of the text, symbolized by a rectangle
            color (Tuple, optional): RGB code for the color of the text. Defaults to (0, 0, 0).
        """
        self._screen.blit(self._font.render(text, 1, color), position)

    def initiate_fire(self):
        """Spawn fires in the generated forest in order to start the burning."""
        nb_fire = self._parameters.nb_initial_fires
        while nb_fire != 0:
            x = random.randint(0, self.GRID_DIM[0] - 1)
            y = random.randint(0, self.GRID_DIM[1] - 1)
            if self._grid._grid[x, y] == 1:
                self._grid._grid[x, y] = 3
                nb_fire -= 1

    def _calculate_probability(self, x: int, y: int):
        """Compute probability for a tree to burn.

        Args:
            x (int): X coordinate of the tree.
            y (int): Y coordinate of the tree.

        Returns:
            [float]: Probability of the tree to burn. Between 0 and 1.
        """
        resistance_tree = self._parameters.resistance_tree1
        if self._grid._grid[x, y] == 2:
            resistance_tree = self._parameters.resistance_tree2
        voisins = self._grid.get_neighbors(x, y)

        [nb_fire3, nb_fire4] = [0, 0]
        for tree in voisins:
            if tree == 3:
                nb_fire3 += 1
            if tree == 4:
                nb_fire4 += 1

        prob = (
            nb_fire3 * self._parameters.transmissibility_fire3
            + nb_fire4 * self._parameters.transmissibility_fire4
        ) / resistance_tree
        prob = min(prob, 1)
        return prob

    def update(self):
        """Update the scene at each frame."""
        for x in range(self.GRID_DIM[0]):
            for y in range(self.GRID_DIM[1]):
                proba = 0
                if self._grid._grid[x, y] == 1 or self._grid._grid[x, y] == 2:
                    proba = self._calculate_probability(x, y)

                # If conditions are satisfied, prepare the tree to be on fire
                index = random.randint(1, 100)
                if index <= proba * 100:
                    self._grid._grid[x, y] = 5

        # Update the value of each tree, to put them on fire or stop the fire
        for x in range(self.GRID_DIM[0]):
            for y in range(self.GRID_DIM[1]):
                if self._grid._grid[x, y] == 4:
                    self._grid._grid[x, y] = 0
                if self._grid._grid[x, y] == 3:
                    self._grid._grid[x, y] = 4
                if self._grid._grid[x, y] == 5:
                    self._grid._grid[x, y] = 3
