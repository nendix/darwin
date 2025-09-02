"""
Darwin - User Interface Components
"""

import pygame
import math
from typing import List, Callable, Any
from ..config import *


class Button:
    """Basic button component"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 callback: Callable = None, color: tuple = GREY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = tuple(min(255, c + 30) for c in color)
        self.is_hovered = False
        self.font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        return False
    
    def draw(self, screen: pygame.Surface):
        """Draw the button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class Slider:
    """Slider component for numeric values"""
    
    def __init__(self, x: int, y: int, width: int, label: str, 
                 min_val: int, max_val: int, initial_val: int):
        self.rect = pygame.Rect(x, y, width, 20)
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value_from_mouse(event.pos[0])
            return True
        return False
    
    def _update_value_from_mouse(self, mouse_x: int):
        """Update value based on mouse position"""
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(self.rect.width, relative_x))
        ratio = relative_x / self.rect.width
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
    
    def draw(self, screen: pygame.Surface):
        """Draw the slider"""
        # Draw label
        label_surface = self.font.render(f"{self.label}: {self.value}", True, WHITE)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Draw slider track
        pygame.draw.rect(screen, GREY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw slider handle
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + ratio * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, 30)
        pygame.draw.rect(screen, WHITE, handle_rect)


class Toggle:
    """Toggle switch component"""
    
    def __init__(self, x: int, y: int, label: str, initial_state: bool = False):
        self.rect = pygame.Rect(x, y, 40, 20)
        self.label = label
        self.state = initial_state
        self.font = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                return True
        return False
    
    def draw(self, screen: pygame.Surface):
        """Draw the toggle"""
        # Draw label
        label_surface = self.font.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.rect.x + 50, self.rect.y))
        
        # Draw toggle background
        color = GREEN if self.state else GREY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw toggle circle
        circle_x = self.rect.x + (30 if self.state else 10)
        circle_y = self.rect.y + 10
        pygame.draw.circle(screen, WHITE, (circle_x, circle_y), 8)


class MenuNavigator:
    """Navigation system for keyboard-controlled menus"""
    
    def __init__(self, items: List[Any]):
        self.items = items
        self.selected_index = 0
    
    def handle_key(self, key: int) -> bool:
        """Handle keyboard navigation"""
        if key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.items)
            return True
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.items)
            return True
        elif key == pygame.K_LEFT:
            item = self.items[self.selected_index]
            if isinstance(item, Slider):
                item.value = max(item.min_val, item.value - 1)
                return True
            elif isinstance(item, Toggle):
                item.state = not item.state
                return True
        elif key == pygame.K_RIGHT:
            item = self.items[self.selected_index]
            if isinstance(item, Slider):
                item.value = min(item.max_val, item.value + 1)
                return True
            elif isinstance(item, Toggle):
                item.state = not item.state
                return True
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            item = self.items[self.selected_index]
            if isinstance(item, Button) and item.callback:
                item.callback()
                return True
            elif isinstance(item, Toggle):
                item.state = not item.state
                return True
        return False
    
    def draw_selection_indicator(self, screen: pygame.Surface):
        """Draw selection indicator for current item"""
        if 0 <= self.selected_index < len(self.items):
            item = self.items[self.selected_index]
            if hasattr(item, 'rect'):
                rect = pygame.Rect(item.rect.x - 10, item.rect.y - 5, 
                                 item.rect.width + 20, item.rect.height + 10)
                pygame.draw.rect(screen, YELLOW, rect, 3)


class HUD:
    """Heads-up display for simulation screen"""
    
    def __init__(self):
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def draw_simulation_hud(self, screen: pygame.Surface, simulation_state: dict):
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
    
    def draw_statistics_summary(self, screen: pygame.Surface, stats: dict, y_start: int = 50):
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
