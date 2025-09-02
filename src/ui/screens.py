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
        self.sliders = [
            Slider(300, 200, 300, "Numero Prede", MIN_PREY_COUNT, MAX_PREY_COUNT, DEFAULT_PREY_COUNT),
            Slider(300, 260, 300, "Numero Predatori", MIN_PREDATOR_COUNT, MAX_PREDATOR_COUNT, DEFAULT_PREDATOR_COUNT),
            Slider(300, 320, 300, "Numero Cibo", MIN_FOOD_COUNT, MAX_FOOD_COUNT, DEFAULT_FOOD_COUNT),
            Slider(300, 380, 300, "Durata (secondi)", MIN_SIMULATION_DURATION, MAX_SIMULATION_DURATION, DEFAULT_SIMULATION_DURATION),
            Slider(300, 440, 300, "Velocità Simulazione", MIN_SIMULATION_SPEED, MAX_SIMULATION_SPEED, DEFAULT_SIMULATION_SPEED)
        ]
        
        self.toggles = [
            Toggle(300, 500, "Mostra Raggio Visivo", False)
        ]
        
        self.buttons = [
            Button(400, 580, 200, 40, "Inizia Simulazione", self.start_simulation),
            Button(400, 640, 200, 40, "Esci", self.quit_game)
        ]
        
        # Combine all interactive elements for navigation
        self.menu_items = self.sliders + self.toggles + self.buttons
        self.navigator = MenuNavigator(self.menu_items)
    
    def start_simulation(self):
        """Start the simulation with current parameters"""
        params = {
            'prey_count': self.sliders[0].value,
            'predator_count': self.sliders[1].value,
            'food_count': self.sliders[2].value,
            'duration': self.sliders[3].value,
            'speed': self.sliders[4].value,
            'show_vision': self.toggles[0].state
        }
        self.screen_manager.start_simulation(params)
    
    def quit_game(self):
        """Quit the application"""
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event: pygame.event.Event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit_game()
            else:
                self.navigator.handle_key(event.key)
        
        # Handle mouse events for UI components
        for item in self.menu_items:
            if hasattr(item, 'handle_event'):
                item.handle_event(event)
    
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
        
        # Draw UI components
        for slider in self.sliders:
            slider.draw(screen)
        
        for toggle in self.toggles:
            toggle.draw(screen)
        
        for button in self.buttons:
            button.draw(screen)
        
        # Draw navigation indicator
        self.navigator.draw_selection_indicator(screen)
        
        # Instructions
        instructions = [
            "Usa le frecce per navigare",
            "Frecce sinistra/destra per modificare valori",
            "Invio/Spazio per selezionare",
            "ESC per uscire"
        ]
        
        y_offset = SCREEN_HEIGHT - 120
        for instruction in instructions:
            text = self.font_small.render(instruction, True, GREY)
            screen.blit(text, (50, y_offset))
            y_offset += 20


class SimulationScreen(Screen):
    """Simulation screen showing the evolution in action"""
    
    def __init__(self, screen_manager, simulation):
        super().__init__(screen_manager)
        self.simulation = simulation
        self.hud = HUD()
        self.camera_x = 0
        self.camera_y = 0
        self.show_vision = simulation.show_vision
        self.paused = False
        
    def handle_event(self, event: pygame.event.Event):
        """Handle simulation events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.screen_manager.show_statistics(self.simulation.get_statistics())
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_v:
                self.show_vision = not self.show_vision
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.simulation.increase_speed()
            elif event.key == pygame.K_MINUS:
                self.simulation.decrease_speed()
            elif event.key == pygame.K_r:
                # Reset camera
                self.camera_x = 0
                self.camera_y = 0
        
        # Camera movement with arrow keys
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.camera_x -= 5
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.camera_x += 5
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.camera_y -= 5
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.camera_y += 5
        
        # Keep camera within bounds
        self.camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, self.camera_x))
        self.camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, self.camera_y))
    
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
        
        # Draw world border
        border_rect = pygame.Rect(-self.camera_x, -self.camera_y, WORLD_WIDTH, WORLD_HEIGHT)
        pygame.draw.rect(screen, GREY, border_rect, 2)
        
        # Draw simulation entities
        camera_offset = (self.camera_x, self.camera_y)
        self.simulation.draw(screen, camera_offset, self.show_vision)
        
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
        
        # Controls help
        controls = [
            "ESC: Menu Statistiche",
            "Spazio: Pausa",
            "V: Toggle Visione",
            "+/-: Velocità",
            "Frecce: Camera",
            "R: Reset Camera"
        ]
        
        y_offset = SCREEN_HEIGHT - 140
        for control in controls:
            text = self.font_small.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 200, y_offset))
            y_offset += 20


class StatisticsScreen(Screen):
    """Statistics screen showing simulation results"""
    
    def __init__(self, screen_manager, statistics):
        super().__init__(screen_manager)
        self.statistics = statistics
        self.hud = HUD()
        
        # Create buttons
        self.buttons = [
            Button(200, 600, 200, 40, "Nuova Simulazione", self.new_simulation),
            Button(420, 600, 200, 40, "Menu Principale", self.back_to_menu),
            Button(640, 600, 200, 40, "Salva Report", self.save_report)
        ]
        
        self.menu_items = self.buttons
        self.navigator = MenuNavigator(self.menu_items)
    
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
            if event.key == pygame.K_ESCAPE:
                self.back_to_menu()
            else:
                self.navigator.handle_key(event.key)
        
        # Handle mouse events for buttons
        for button in self.buttons:
            button.handle_event(event)
    
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
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        
        # Draw navigation indicator
        self.navigator.draw_selection_indicator(screen)


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
