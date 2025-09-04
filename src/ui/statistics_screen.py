"""
Darwin - Statistics Screen
"""

import pygame
from ..analysis import StatisticsAnalyzer
from ..config import *


class StatisticsScreen:
    """Statistics screen showing simulation results"""
    
    def __init__(self, app, statistics):
        self.app = app
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.statistics = statistics
        
        # Simple menu options
        self.menu_options = [
            {"name": "Nuova Simulazione", "action": self.new_simulation},
            {"name": "Menu Principale", "action": self.back_to_menu},
            {"name": "Salva Report", "action": self.save_report}
        ]
        
        self.selected_index = 0
    
    def new_simulation(self):
        """Start a new simulation with same parameters"""
        self.app.restart_simulation()
    
    def back_to_menu(self):
        """Return to main menu"""
        self.app.show_menu()
    
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
        y_offset = self._draw_statistics_summary(screen, self.statistics, 100)
        
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
    
    def _draw_statistics_summary(self, screen: pygame.Surface, stats: dict, y_start: int = 50):
        """Draw statistics summary"""
        y_offset = y_start
        
        # Generation info
        generation = stats.get('generation', 1)
        gen_text = self.font_large.render(f"Generazione: {generation}", True, WHITE)
        screen.blit(gen_text, (50, y_offset))
        y_offset += 40
        
        # Survival stats
        if 'survival_stats' in stats:
            survival = stats['survival_stats']
            survival_text = self.font_medium.render("Statistiche di Sopravvivenza:", True, WHITE)
            screen.blit(survival_text, (50, y_offset))
            y_offset += 30
            
            predator_survival = survival.get('predator_survival_rate', 0)
            prey_survival = survival.get('prey_survival_rate', 0)
            
            pred_text = self.font_small.render(f"Sopravvivenza Predatori: {predator_survival:.1f}%", True, RED)
            prey_text = self.font_small.render(f"Sopravvivenza Prede: {prey_survival:.1f}%", True, BLUE)
            
            screen.blit(pred_text, (70, y_offset))
            screen.blit(prey_text, (70, y_offset + 25))
            y_offset += 60
        
        return y_offset
