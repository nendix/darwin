"""
Darwin - Food Entity
"""

import pygame
from typing import Tuple

from ..config import *


class Food:
    """Food entity for prey to consume"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.alive = True
        self.energy_value = FOOD_ENERGY_GAIN
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[int, int], show_vision: bool = False):
        """Draw food as a small green circle"""
        screen_x = int(self.x - camera_offset[0])
        screen_y = int(self.y - camera_offset[1])
        
        if 0 <= screen_x <= SCREEN_WIDTH and 0 <= screen_y <= SCREEN_HEIGHT:
            pygame.draw.circle(screen, GREEN, (screen_x, screen_y), FOOD_RADIUS)
    
    def update(self, dt, entities_nearby=None):
        """Update food - food doesn't need to do anything in update"""
        pass
