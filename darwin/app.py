
import pygame
from typing import Dict, Any
from .ui import MenuScreen, SimulationScreen, StatisticsScreen
from .simulation.simulation import Simulation
from darwin.config import SCREEN_WIDTH, SCREEN_HEIGHT

class DarwinApp:

    def __init__(self):
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
        self.simulation_params = params
        simulation = Simulation(params)
        self.current_screen = SimulationScreen(self, simulation)

    def show_statistics(self, statistics: Dict[str, Any]):
        self.current_screen = StatisticsScreen(self, statistics)

    def restart_simulation(self):
        if self.simulation_params:
            self.start_simulation(self.simulation_params)

    def show_menu(self):
        self.current_screen = self.menu_screen

    def run(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            # Pass events to current screen
            if self.current_screen:
                self.current_screen.handle_event(event)

    def _draw(self):
        if self.current_screen:
            self.current_screen.draw(self.screen)

    def quit(self):
        self.running = False
