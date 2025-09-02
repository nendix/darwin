"""
Darwin - Base Screen Class
"""

import pygame
from ..config import *


class Screen:
    """Base class for all screens"""
    
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle screen-specific events"""
        pass
    
    def update(self, dt: float):
        """Update screen state"""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Draw the screen"""
        pass
