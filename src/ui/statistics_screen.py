import pygame
from ..analysis import StatisticsAnalyzer
from ..config import *
from .ui_utils import draw_text, text_width


class StatisticsScreen:
    """Statistics screen showing simulation results"""

    def __init__(self, app, statistics):
        self.app = app
        self.statistics = statistics

    def new_simulation(self):
        """Start a new simulation with same parameters"""
        self.app.restart_simulation()

    def back_to_menu(self):
        """Return to main menu"""
        self.app.show_menu()

    def save_report(self):
        """Save comprehensive simulation report"""
        try:
            report_path = StatisticsAnalyzer.generate_comprehensive_report(
                self.statistics
            )
            print(f"Report salvato in: {report_path}")
        except Exception as e:
            print(f"Errore nel salvare il report: {e}")

    def handle_event(self, event: pygame.event.Event):
        """Handle statistics screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # Q: Chiudere l'app
                pygame.quit()
                import sys

                sys.exit()
            elif event.key == pygame.K_m:
                # M: Tornare al menu
                self.back_to_menu()
            elif event.key == pygame.K_s:
                # S: Salvare i reports
                self.save_report()

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        """Draw statistics screen"""
        screen.fill(BLACK)

        # Title
        title_text = "STATISTICHE SIMULAZIONE"
        draw_text(screen, title_text, 50, 50, WHITE, FONT_SIZE_LARGE)

        # Draw statistics summary
        y_offset = self._draw_statistics_summary(screen, self.statistics, 100)

        # Draw final populations
        if "final_populations" in self.statistics:
            populations = self.statistics["final_populations"]

            draw_text(screen, "Popolazioni:", 50, y_offset, WHITE, FONT_SIZE_LARGE)
            y_offset += 35

            predators = populations.get("predators", 0)
            prey = populations.get("prey", 0)

            draw_text(
                screen,
                f"Predatori: {predators}",
                70,
                y_offset,
                RED,
                FONT_SIZE_MEDIUM,
            )
            draw_text(
                screen,
                f"Prede: {prey}",
                70,
                y_offset + 25,
                BLUE,
                FONT_SIZE_MEDIUM,
            )
            y_offset += 60

        # Evolution info
        if "evolution_info" in self.statistics:
            evolution = self.statistics["evolution_info"]

            draw_text(
                screen,
                "Evoluzione:",
                50,
                y_offset,
                WHITE,
                FONT_SIZE_LARGE,
            )
            y_offset += 35

            reproductions = evolution.get("total_reproductions", 0)

            draw_text(
                screen,
                f"Riproduzioni: {reproductions}",
                70,
                y_offset,
                WHITE,
                FONT_SIZE_MEDIUM,
            )

        # Instructions
        instructions = [
            "Q - Chiudere applicazione",
            "M - Menu principale",
            "S - Salvare report",
        ]

        y_offset = SCREEN_HEIGHT - 100
        for instruction in instructions:
            draw_text(screen, instruction, 50, y_offset, GREY, FONT_SIZE_SMALL)
            y_offset += 25

    def _draw_statistics_summary(
        self, screen: pygame.Surface, stats: dict, y_start: int = 50
    ):
        """Draw statistics summary"""
        y_offset = y_start

        if "survival_stats" in stats:
            survival = stats["survival_stats"]
            draw_text(
                screen,
                "Sopravvivenza:",
                50,
                y_offset,
                WHITE,
                FONT_SIZE_LARGE,
            )
            y_offset += 30

            predator_survival = survival.get("predator_survival_rate", 0)
            prey_survival = survival.get("prey_survival_rate", 0)

            draw_text(
                screen,
                f"Predatori: {predator_survival:.1f}%",
                70,
                y_offset,
                RED,
                FONT_SIZE_MEDIUM,
            )
            draw_text(
                screen,
                f"Prede: {prey_survival:.1f}%",
                70,
                y_offset + 25,
                BLUE,
                FONT_SIZE_MEDIUM,
            )
            y_offset += 60

        return y_offset
