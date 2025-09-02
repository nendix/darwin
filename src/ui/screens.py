"""
Darwin - Screen Management
"""

import pygame
import sys
import os
from abc import ABC, abstractmethod
from typing import Dict, Any

from ..config import *
from .components import Button, Slider, Toggle, MenuNavigator, HUD
from ..analysis import StatisticsAnalyzer


class Screen(ABC):
    """Base class for all screens"""
    
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle screen-specific events"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update screen state"""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Draw the screen"""
        pass


class MenuScreen(Screen):
    """Main menu screen with simulation parameters"""
    
    def __init__(self, screen_manager):
        super().__init__(screen_manager)
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
        self.screen_manager.start_simulation(params)
    
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


class StatisticsScreen(Screen):
    """Statistics screen showing simulation results"""
    
    def __init__(self, screen_manager, statistics):
        super().__init__(screen_manager)
        self.statistics = statistics
        self.hud = HUD()
        
        # Simple menu options
        self.menu_options = [
            {"name": "Nuova Simulazione", "action": self.new_simulation},
            {"name": "Menu Principale", "action": self.back_to_menu},
            {"name": "Salva Report", "action": self.save_report}
        ]
        
        self.selected_index = 0
    
    def new_simulation(self):
        """Start a new simulation with same parameters"""
        self.screen_manager.restart_simulation()
    
    def back_to_menu(self):
        """Return to main menu"""
        self.screen_manager.set_screen('menu')
    
    def save_report(self):
        """Save comprehensive simulation report"""
        try:
            report_path = StatisticsAnalyzer.generate_comprehensive_report(self.statistics)
            print(f"Report salvato in: {report_path}")
        except Exception as e:
            print(f"Errore nel salvare il report: {e}")
    
    def handle_event(self, event: pygame.event.Event):
        """Handle statistics screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.back_to_menu()
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_SPACE:
                self.menu_options[self.selected_index]["action"]()
    
    def update(self, dt: float):
        """Update statistics (nothing to update)"""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Draw statistics screen"""
        screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("STATISTICHE SIMULAZIONE", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Draw statistics summary
        y_offset = self.hud.draw_statistics_summary(screen, self.statistics, 100)
        
        # Draw final populations
        if 'final_populations' in self.statistics:
            populations = self.statistics['final_populations']
            
            pop_title = self.font_medium.render("Popolazioni Finali:", True, WHITE)
            screen.blit(pop_title, (50, y_offset))
            y_offset += 35
            
            predators = populations.get('predators', 0)
            prey = populations.get('prey', 0)
            
            pred_text = self.font_small.render(f"Predatori sopravvissuti: {predators}", True, RED)
            prey_text = self.font_small.render(f"Prede sopravvissute: {prey}", True, BLUE)
            
            screen.blit(pred_text, (70, y_offset))
            screen.blit(prey_text, (70, y_offset + 25))
            y_offset += 60
        
        # Evolution info
        if 'evolution_info' in self.statistics:
            evolution = self.statistics['evolution_info']
            
            evo_title = self.font_medium.render("Informazioni Evoluzione:", True, WHITE)
            screen.blit(evo_title, (50, y_offset))
            y_offset += 35
            
            reproductions = evolution.get('total_reproductions', 0)
            mutations = evolution.get('total_mutations', 0)
            
            repr_text = self.font_small.render(f"Riproduzioni totali: {reproductions}", True, WHITE)
            mut_text = self.font_small.render(f"Mutazioni totali: {mutations}", True, WHITE)
            
            screen.blit(repr_text, (70, y_offset))
            screen.blit(mut_text, (70, y_offset + 25))
        
        # Draw menu options
        y_options_start = 500
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_index else WHITE
            option_surface = self.font_medium.render(option["name"], True, color)
            screen.blit(option_surface, (300, y_options_start + i * 40))
        
        # Instructions
        instructions = [
            "↑/↓ - Navigare",
            "SPAZIO - Selezionare",
            "Q - Menu Principale"
        ]
        
        y_offset = SCREEN_HEIGHT - 100
        for instruction in instructions:
            text = self.font_small.render(instruction, True, GREY)
            screen.blit(text, (50, y_offset))
            y_offset += 25


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
        
        self.simulation_params = params
        simulation = Simulation(params)
        
        sim_screen = SimulationScreen(self, simulation)
        self.screens['simulation'] = sim_screen
        self.set_screen('simulation')
    
    def show_statistics(self, statistics: Dict[str, Any]):
        """Show statistics screen"""
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
