import pygame
from ..config import *
from .ui_utils import draw_text, text_width


class SimulationScreen:
    """Simulation screen showing the evolution in action"""

    def __init__(self, app, simulation):
        self.app = app
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
            "predator_count": len(
                [
                    e
                    for e in self.simulation.entities
                    if e.__class__.__name__ == "Predator" and e.alive
                ]
            ),
            "prey_count": len(
                [
                    e
                    for e in self.simulation.entities
                    if e.__class__.__name__ == "Prey" and e.alive
                ]
            ),
            "time_remaining": self.simulation.time_remaining,
            "speed": self.simulation.speed,
        }
        self._draw_simulation_hud(screen, simulation_state)

        # Pause indicator
        if self.paused:
            pause_text = "PAUSA"
            pause_x = (SCREEN_WIDTH - text_width(pause_text, FONT_SIZE_LARGE)) // 2
            draw_text(
                screen, pause_text, pause_x, SCREEN_HEIGHT // 2, YELLOW, FONT_SIZE_LARGE
            )

        # Controls help (simplified)
        controls = [
            "Q: Esci",
            "Spazio: Pausa",
            "V: Toggle Visione",
            "+/-: Velocità",
        ]

        y_offset = SCREEN_HEIGHT - 100
        for control in controls:
            draw_text(screen, control, 20, y_offset, WHITE, FONT_SIZE_SMALL)
            y_offset += 20

    def _draw_simulation_hud(self, screen: pygame.Surface, simulation_state: dict):
        """Draw HUD for simulation screen"""

        y_offset = 20

        # Population counts
        predator_count = simulation_state.get("predator_count", 0)
        prey_count = simulation_state.get("prey_count", 0)

        draw_text(
            screen, f"Predatori: {predator_count}", 20, y_offset, RED, FONT_SIZE_MEDIUM
        )
        draw_text(
            screen, f"Prede: {prey_count}", 20, y_offset + 25, BLUE, FONT_SIZE_MEDIUM
        )

        # Time remaining
        time_remaining = simulation_state.get("time_remaining", 0)
        minutes = int(time_remaining // 60)
        seconds = int(time_remaining % 60)
        draw_text(
            screen,
            f"Tempo: {minutes:02d}:{seconds:02d}",
            20,
            y_offset + 50,
            WHITE,
            FONT_SIZE_MEDIUM,
        )

        # Speed indicator
        speed = simulation_state.get("speed", 1)
        draw_text(
            screen, f"Velocità: {speed}x", 20, y_offset + 75, WHITE, FONT_SIZE_SMALL
        )

