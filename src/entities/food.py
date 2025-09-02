"""
Darwin - Food Entity
"""

import pygame
from typing import List, Tuple

from .base_entity import Entity
from ..config import *


class Food(Entity):
    """Food entity for prey to consume"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.energy_value = FOOD_ENERGY_GAIN
    
    def update(self, dt: float, entities: List[Entity]):
        """Food doesn't move or change"""
        pass
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[int, int], show_vision: bool = False):
        """Draw food as a small green circle"""
        screen_x = int(self.x)
        screen_y = int(self.y)
        
        if 0 <= screen_x <= SCREEN_WIDTH and 0 <= screen_y <= SCREEN_HEIGHT:
            pygame.draw.circle(screen, GREEN, (screen_x, screen_y), FOOD_RADIUS)
