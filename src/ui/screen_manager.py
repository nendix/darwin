"""
Darwin - Screen Manager
"""

import pygame
from typing import Dict, Any
from .base_screen import Screen


class ScreenManager:
    """Manages different screens and transitions"""
    
    def __init__(self):
        self.screens = {}
        self.current_screen = None
        self.simulation_params = None
        
    def add_screen(self, name: str, screen: Screen):
        """Add a screen to the manager"""
        self.screens[name] = screen
        
    def set_screen(self, name: str):
        """Switch to a specific screen"""
        if name in self.screens:
            self.current_screen = self.screens[name]
    
    def start_simulation(self, params: Dict[str, Any]):
        """Start simulation with given parameters"""
        from ..simulation.simulation import Simulation
        from .simulation_screen import SimulationScreen
        
        self.simulation_params = params
        simulation = Simulation(params)
        
        sim_screen = SimulationScreen(self, simulation)
        self.screens['simulation'] = sim_screen
        self.set_screen('simulation')
    
    def show_statistics(self, statistics: Dict[str, Any]):
        """Show statistics screen"""
        from .statistics_screen import StatisticsScreen
        
        stats_screen = StatisticsScreen(self, statistics)
        self.screens['statistics'] = stats_screen
        self.set_screen('statistics')
    
    def restart_simulation(self):
        """Restart simulation with same parameters"""
        if self.simulation_params:
            self.start_simulation(self.simulation_params)
    
    def handle_event(self, event: pygame.event.Event):
        """Handle events for current screen"""
        if self.current_screen:
            self.current_screen.handle_event(event)
    
    def update(self, dt: float):
        """Update current screen"""
        if self.current_screen:
            self.current_screen.update(dt)
    
    def draw(self, screen: pygame.Surface):
        """Draw current screen"""
        if self.current_screen:
            self.current_screen.draw(screen)
