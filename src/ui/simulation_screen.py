"""
Darwin - Simulation Screen
"""

import pygame
from .base_screen import Screen
from .components import HUD
from ..config import *


class SimulationScreen(Screen):
    """Simulation screen showing the evolution in action"""
    
    def __init__(self, screen_manager, simulation):
        super().__init__(screen_manager)
        self.simulation = simulation
        self.hud = HUD()
        self.show_vision = simulation.show_vision
        self.paused = False
        
    def handle_event(self, event: pygame.event.Event):
        """Handle simulation events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.screen_manager.show_statistics(self.simulation.get_statistics())
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_v:
                self.show_vision = not self.show_vision
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.simulation.increase_speed()
            elif event.key == pygame.K_MINUS:
                self.simulation.decrease_speed()
    
    def update(self, dt: float):
        """Update simulation"""
        if not self.paused:
            self.simulation.update(dt)
            
        # Check if simulation is finished
        if self.simulation.is_finished():
            self.screen_manager.show_statistics(self.simulation.get_statistics())
    
    def draw(self, screen: pygame.Surface):
        """Draw simulation screen"""
        screen.fill(BLACK)
        
        # Draw simulation entities (no camera offset needed)
        self.simulation.draw(screen, (0, 0), self.show_vision)
        
        # Draw HUD
        simulation_state = {
            'predator_count': len([e for e in self.simulation.entities if e.__class__.__name__ == 'Predator' and e.alive]),
            'prey_count': len([e for e in self.simulation.entities if e.__class__.__name__ == 'Prey' and e.alive]),
            'food_count': len([e for e in self.simulation.entities if e.__class__.__name__ == 'Food' and e.alive]),
            'time_remaining': self.simulation.time_remaining,
            'speed': self.simulation.speed
        }
        self.hud.draw_simulation_hud(screen, simulation_state)
        
        # Pause indicator
        if self.paused:
            pause_text = self.font_large.render("PAUSA", True, YELLOW)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
        
        # Controls help (simplified)
        controls = [
            "Q: Statistiche",
            "Spazio: Pausa",
            "V: Toggle Visione",
            "+/-: Velocità"
        ]
        
        y_offset = SCREEN_HEIGHT - 100
        for control in controls:
            text = self.font_small.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 150, y_offset))
            y_offset += 20
