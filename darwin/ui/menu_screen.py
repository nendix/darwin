import pygame
import sys
from darwin import config as c
from .ui_utils import draw_text, text_width


class MenuScreen:
    """Main menu screen with simulation parameters"""

    def __init__(self, app):
        self.app = app
        self.key_repeat_delay = 0
        self.setup_ui()

    def setup_ui(self):
        """Setup menu UI components"""
        # Simple text-based menu parameters
        self.parameters = [
            {
                "name": "Prede",
                "value": c.DEFAULT_PREY_COUNT,
                "min": c.MIN_PREY_COUNT,
                "max": c.MAX_PREY_COUNT,
            },
            {
                "name": "Predatori",
                "value": c.DEFAULT_PREDATOR_COUNT,
                "min": c.MIN_PREDATOR_COUNT,
                "max": c.MAX_PREDATOR_COUNT,
            },
            {
                "name": "Cibo",
                "value": c.DEFAULT_FOOD_COUNT,
                "min": c.MIN_FOOD_COUNT,
                "max": c.MAX_FOOD_COUNT,
            },
            {
                "name": "Durata (secondi)",
                "value": c.DEFAULT_SIMULATION_DURATION,
                "min": c.MIN_SIMULATION_DURATION,
                "max": c.MAX_SIMULATION_DURATION,
            },
            {
                "name": "Velocità Simulazione",
                "value": c.DEFAULT_SIMULATION_SPEED,
                "min": c.MIN_SIMULATION_SPEED,
                "max": c.MAX_SIMULATION_SPEED,
            },
            {"name": "Raggio Visivo", "value": False, "type": "toggle"},
        ]

        self.selected_index = 0

    def _modify_parameter(self, direction):
        """Modify the selected parameter"""
        param = self.parameters[self.selected_index]

        if param.get("type") == "toggle":
            # Toggle boolean value
            param["value"] = not param["value"]
        else:
            # Adjust numeric value
            step = 1
            if param["name"] == "Cibo":
                step = 5  # Larger steps for food count
            elif param["name"] == "Durata (secondi)":
                step = 10  # 10 second steps for duration

            new_value = param["value"] + (direction * step)
            param["value"] = max(param["min"], min(param["max"], new_value))

    def start_simulation(self):
        """Start the simulation with current parameters"""
        params = {
            "prey_count": self.parameters[0]["value"],
            "predator_count": self.parameters[1]["value"],
            "food_count": self.parameters[2]["value"],
            "duration": self.parameters[3]["value"],
            "speed": self.parameters[4]["value"],
            "show_vision": self.parameters[5]["value"],
        }
        self.app.start_simulation(params)

    def quit_game(self):
        """Quit the application"""
        pygame.quit()
        sys.exit()

    def handle_event(self, event: pygame.event.Event):
        """Handle both discrete events and continuous input"""
        # Handle discrete events
        if event.type == pygame.QUIT:
            self.quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.quit_game()
            elif event.key == pygame.K_SPACE:
                self.start_simulation()

        # Handle continuous input with timing control
        if self.key_repeat_delay <= 0:
            keys = pygame.key.get_pressed()

            # Navigation
            if keys[pygame.K_k] or keys[pygame.K_UP]:
                self.selected_index = max(0, self.selected_index - 1)
                self.key_repeat_delay = 8
            elif keys[pygame.K_j] or keys[pygame.K_DOWN]:
                self.selected_index = min(
                    len(self.parameters) - 1, self.selected_index + 1
                )
                self.key_repeat_delay = 8

            # Parameter adjustment
            if keys[pygame.K_h] or keys[pygame.K_LEFT]:
                direction = -1
                self._modify_parameter(direction)
                self.key_repeat_delay = 4
            elif keys[pygame.K_l] or keys[pygame.K_RIGHT]:
                direction = 1
                self._modify_parameter(direction)
                self.key_repeat_delay = 4
        else:
            self.key_repeat_delay -= 1

    def update(self, dt: float):
        """Update menu - key repeat timing is now handled in handle_event"""
        self.handle_event(pygame.event.Event)
        pass

    def draw(self, screen: pygame.Surface):
        """Draw the menu screen"""
        screen.fill(c.BLACK)

        # Title
        title_text = "DARWIN - Simulatore Evoluzione"
        title_x = (c.SCREEN_WIDTH - text_width(title_text, c.FONT_SIZE_LARGE)) // 2
        draw_text(screen, title_text, title_x, 100, c.WHITE, c.FONT_SIZE_LARGE)

        # Subtitle
        subtitle_text = "Configura i parametri della simulazione"
        subtitle_x = (
            c.SCREEN_WIDTH - text_width(subtitle_text, c.FONT_SIZE_MEDIUM)
        ) // 2
        draw_text(screen, subtitle_text, subtitle_x, 140, c.GREY, c.FONT_SIZE_MEDIUM)

        # Parameters
        y_start = 220

        # Calculate center position for parameters - fixed row width approach
        # Row width: longest name + gap + value area
        max_name_width = 0
        for param in self.parameters:
            name_width = text_width(param["name"], c.FONT_SIZE_MEDIUM)
            max_name_width = max(max_name_width, name_width)

        gap_width = (
            60  # Fixed gap between name and value (no spaces, just coordinate offset)
        )
        value_area_width = 80  # Fixed width for value area
        row_width = max_name_width + gap_width + value_area_width
        center_x = (c.SCREEN_WIDTH - row_width) // 2

        for i, param in enumerate(self.parameters):
            color = c.YELLOW if i == self.selected_index else c.WHITE

            # Draw parameter name (left-aligned from center position)
            name_x = center_x
            draw_text(
                screen,
                param["name"],
                name_x,
                y_start + i * 40,
                color,
                c.FONT_SIZE_MEDIUM,
            )

            # Draw parameter value (right-aligned in the value area)
            if param.get("type") == "toggle":
                value_text = "ON" if param["value"] else "OFF"
            else:
                value_text = str(param["value"])

            # Calculate right-aligned position for value
            value_text_width = text_width(value_text, c.FONT_SIZE_MEDIUM)
            value_x = (
                center_x
                + max_name_width
                + gap_width
                + value_area_width
                - value_text_width
            )
            draw_text(
                screen,
                value_text,
                value_x,
                y_start + i * 40,
                color,
                c.FONT_SIZE_MEDIUM,
            )

        # Start instruction
        start_text = "Premi SPACE per iniziare"
        start_x = (c.SCREEN_WIDTH - text_width(start_text, c.FONT_SIZE_MEDIUM)) // 2
        draw_text(
            screen,
            start_text,
            start_x,
            y_start + len(self.parameters) * 40 + 60,
            c.GREEN,
            c.FONT_SIZE_MEDIUM,
        )

        # Instructions
        instructions = [
            "UP/DOWN o K/J - Navigare tra parametri",
            "LEFT/RIGHT o H/L - Modificare valori",
            "SPACE - Iniziare simulazione",
            "Q - Uscire",
        ]

        # Find the longest instruction for centering
        max_instruction_width = 0
        for instruction in instructions:
            width = text_width(instruction, c.FONT_SIZE_SMALL)
            max_instruction_width = max(max_instruction_width, width)

        # Center the instructions block
        instructions_start_x = (c.SCREEN_WIDTH - max_instruction_width) // 2

        y_offset = c.SCREEN_HEIGHT - 120
        for instruction in instructions:
            draw_text(
                screen,
                instruction,
                instructions_start_x,
                y_offset,
                c.GREY,
                c.FONT_SIZE_SMALL,
            )
            y_offset += 25
