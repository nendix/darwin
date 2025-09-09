"""
Darwin - Food Entity
"""

import pygame
from typing import Tuple

from darwin import config as c


class Food:
    """Food entity for prey to consume"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.alive = True
        self.energy_value = c.FOOD_ENERGY_GAIN

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset: Tuple[int, int],
        show_vision: bool = False,
    ):
        """Draw food as a small green circle"""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])

        if 0 <= screen_x <= c.SCREEN_WIDTH and 0 <= screen_y <= c.SCREEN_HEIGHT:
            pygame.draw.circle(screen, c.GREEN, (screen_x, screen_y), c.FOOD_RADIUS)

    def update(self, dt, entities_nearby=None):
        """Update food - food doesn't need to do anything in update"""
        pass
