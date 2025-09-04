"""
Darwin - Main Application Class
"""

import pygame
import sys
from typing import Dict, Any
from .ui import MenuScreen, SimulationScreen, StatisticsScreen
from .simulation.simulation import Simulation
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
        
        # Screen management
        self.current_screen = None
        self.simulation_params = None
        
        # Create menu screen
        self.menu_screen = MenuScreen(self)
        self.current_screen = self.menu_screen
        
        # Initialize fonts
        pygame.font.init()
    
    def start_simulation(self, params: Dict[str, Any]):
        """Start simulation with given parameters"""
        self.simulation_params = params
        simulation = Simulation(params)
        self.current_screen = SimulationScreen(self, simulation)
    
    def show_statistics(self, statistics: Dict[str, Any]):
        """Show statistics screen"""
        self.current_screen = StatisticsScreen(self, statistics)
    
    def restart_simulation(self):
        """Restart simulation with same parameters"""
        if self.simulation_params:
            self.start_simulation(self.simulation_params)
    
    def show_menu(self):
        """Return to main menu"""
        self.current_screen = self.menu_screen
    
    def run(self):
        """Main application loop"""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            
            # Handle events
            self._handle_events()
            
            # Update current screen
            if self.current_screen:
                self.current_screen.update(dt)
            
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
            
            # Pass events to current screen
            if self.current_screen:
                self.current_screen.handle_event(event)
    
    def _draw(self):
        """Draw the current screen"""
        if self.current_screen:
            self.current_screen.draw(self.screen)
    
    def quit(self):
        """Quit the application"""
        self.running = False
