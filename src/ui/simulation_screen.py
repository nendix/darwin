"""
Darwin - Simulation Screen
"""

import pygame
from ..config import *


class SimulationScreen:
    """Simulation screen showing the evolution in action"""
    
    def __init__(self, app, simulation):
        self.app = app
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.simulation = simulation
        self.show_vision = simulation.show_vision
        self.paused = False
        
    def handle_event(self, event: pygame.event.Event):
        """Handle simulation events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.app.show_statistics(self.simulation.get_statistics())
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
            self.app.show_statistics(self.simulation.get_statistics())
    
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
        self._draw_simulation_hud(screen, simulation_state)
        
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
    
    def _draw_simulation_hud(self, screen: pygame.Surface, simulation_state: dict):
        """Draw HUD for simulation screen"""
        # Background panel
        panel_rect = pygame.Rect(10, 10, 300, 120)
        pygame.draw.rect(screen, BLACK, panel_rect)
        pygame.draw.rect(screen, WHITE, panel_rect, 2)
        
        y_offset = 20
        
        # Population counts
        predator_count = simulation_state.get('predator_count', 0)
        prey_count = simulation_state.get('prey_count', 0)
        food_count = simulation_state.get('food_count', 0)
        
        predator_text = self.font_medium.render(f"Predatori: {predator_count}", True, RED)
        prey_text = self.font_medium.render(f"Prede: {prey_count}", True, BLUE)
        food_text = self.font_medium.render(f"Cibo: {food_count}", True, GREEN)
        
        screen.blit(predator_text, (20, y_offset))
        screen.blit(prey_text, (20, y_offset + 25))
        screen.blit(food_text, (20, y_offset + 50))
        
        # Time remaining
        time_remaining = simulation_state.get('time_remaining', 0)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        time_text = self.font_medium.render(f"Tempo: {minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(time_text, (20, y_offset + 75))
        
        # Speed indicator
        speed = simulation_state.get('speed', 1)
        speed_text = self.font_small.render(f"Velocità: {speed}x", True, WHITE)
        screen.blit(speed_text, (220, y_offset + 100))