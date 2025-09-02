"""
Darwin - Main Application Class
"""

import pygame
import sys
from .ui.screens import ScreenManager, MenuScreen
from .config import *


class DarwinApp:
    """Main application class that manages the entire Darwin simulation"""
    
    def __init__(self):
        """Initialize the Darwin application"""
        # Initialize Pygame
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Darwin - Simulatore di Evoluzione")
        
        # Setup clock for frame rate control
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize screen manager
        self.screen_manager = ScreenManager()
        
        # Create and add screens
        menu_screen = MenuScreen(self.screen_manager)
        self.screen_manager.add_screen('menu', menu_screen)
        self.screen_manager.set_screen('menu')
        
        # Initialize fonts
        pygame.font.init()
    
    def run(self):
        """Main application loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            # Handle events
            self._handle_events()
            
            # Update current screen
            self.screen_manager.update(dt)
            
            # Draw everything
            self._draw()
            
            # Update display
            pygame.display.flip()
    
    def _handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            
            # Pass events to screen manager
            self.screen_manager.handle_event(event)
    
    def _draw(self):
        """Draw the current screen"""
        self.screen_manager.draw(self.screen)
    
    def quit(self):
        """Quit the application"""
        self.running = False
