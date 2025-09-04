"""
Darwin - Menu Screen
"""

import pygame
import sys
from ..config import *


class MenuScreen:
    """Main menu screen with simulation parameters"""
    
    def __init__(self, app):
        self.app = app
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup menu UI components"""
        # Simple text-based menu parameters
        self.parameters = [
            {"name": "Numero Prede", "value": DEFAULT_PREY_COUNT, "min": MIN_PREY_COUNT, "max": MAX_PREY_COUNT},
            {"name": "Numero Predatori", "value": DEFAULT_PREDATOR_COUNT, "min": MIN_PREDATOR_COUNT, "max": MAX_PREDATOR_COUNT},
            {"name": "Numero Cibo", "value": DEFAULT_FOOD_COUNT, "min": MIN_FOOD_COUNT, "max": MAX_FOOD_COUNT},
            {"name": "Durata (secondi)", "value": DEFAULT_SIMULATION_DURATION, "min": MIN_SIMULATION_DURATION, "max": MAX_SIMULATION_DURATION},
            {"name": "Velocità Simulazione", "value": DEFAULT_SIMULATION_SPEED, "min": MIN_SIMULATION_SPEED, "max": MAX_SIMULATION_SPEED},
            {"name": "Mostra Raggio Visivo", "value": False, "type": "toggle"}
        ]
        
        self.selected_index = 0
    
    def start_simulation(self):
        """Start the simulation with current parameters"""
        params = {
            'prey_count': self.parameters[0]['value'],
            'predator_count': self.parameters[1]['value'],
            'food_count': self.parameters[2]['value'],
            'duration': self.parameters[3]['value'],
            'speed': self.parameters[4]['value'],
            'show_vision': self.parameters[5]['value']
        }
        self.app.start_simulation(params)
    
    def quit_game(self):
        """Quit the application"""
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event: pygame.event.Event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.quit_game()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.parameters)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.parameters)
            elif event.key == pygame.K_LEFT:
                self._modify_parameter(-1)
            elif event.key == pygame.K_RIGHT:
                self._modify_parameter(1)
            elif event.key == pygame.K_SPACE:
                self.start_simulation()
    
    def _modify_parameter(self, direction):
        """Modify the selected parameter"""
        param = self.parameters[self.selected_index]
        
        if param.get("type") == "toggle":
            # Toggle boolean value
            param["value"] = not param["value"]
        else:
            # Adjust numeric value
            step = 1
            if param["name"] == "Numero Cibo":
                step = 5  # Larger steps for food count
            elif param["name"] == "Durata (secondi)":
                step = 10  # 10 second steps for duration
            
            new_value = param["value"] + (direction * step)
            param["value"] = max(param["min"], min(param["max"], new_value))
    
    def update(self, dt: float):
        """Update menu (nothing to update)"""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Draw the menu screen"""
        screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("DARWIN - Simulatore Evoluzione", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Configura i parametri della simulazione", True, GREY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 140))
        screen.blit(subtitle, subtitle_rect)
        
        # Parameters
        y_start = 220
        for i, param in enumerate(self.parameters):
            color = YELLOW if i == self.selected_index else WHITE
            
            if param.get("type") == "toggle":
                value_text = "Sì" if param["value"] else "No"
                text = f"{param['name']}: {value_text}"
            else:
                text = f"{param['name']}: {param['value']}"
            
            param_surface = self.font_medium.render(text, True, color)
            screen.blit(param_surface, (300, y_start + i * 40))
        
        # Start instruction
        start_text = self.font_medium.render("Premi SPAZIO per iniziare", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, y_start + len(self.parameters) * 40 + 60))
        screen.blit(start_text, start_rect)
        
        # Instructions
        instructions = [
            "↑/↓ - Navigare tra parametri",
            "←/→ - Modificare valori",
            "SPAZIO - Iniziare simulazione",
            "Q - Uscire"
        ]
        
        y_offset = SCREEN_HEIGHT - 120
        for instruction in instructions:
            text = self.font_small.render(instruction, True, GREY)
            screen.blit(text, (50, y_offset))
            y_offset += 25
