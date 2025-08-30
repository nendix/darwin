import pygame as pg
import sys
from .common import draw_text, text_width
from .style import BLACK, WHITE, GREY, YELLOW
from ..config import save_params
from ..utils import clamp


def get_parameter_info():
    return [
        {
            "key": "population_prey",
            "display_name": "Prey Population",
            "min": 4,
            "max": 500,
            "step": 1,
        },
        {
            "key": "population_pred",
            "display_name": "Predator Population",
            "min": 2,
            "max": 100,
            "step": 1,
        },
        {
            "key": "food_count",
            "display_name": "Food Amount",
            "min": 4,
            "max": 500,
            "step": 1,
        },
        {
            "key": "generations",
            "display_name": "Generations",
            "min": 1,
            "max": 100,
            "step": 1,
        },
        {
            "key": "steps_per_generation",
            "display_name": "Steps per Generation",
            "min": 100,
            "max": 3000,
            "step": 100,
        },
        {
            "key": "sim_speed",
            "display_name": "Simulation Speed",
            "min": 1,
            "max": 12,
            "step": 1,
        },
        {
            "key": "draw_vision",
            "display_name": "Show Vision",
            "min": False,
            "max": True,
            "step": 1,
        },
    ]


def draw_parameter_row(screen, param_info, value, x, y, is_selected=False):
    # Parameter name
    text_color = YELLOW if is_selected else WHITE
    draw_text(screen, param_info["display_name"], x, y, text_color, 28)

    # Value display and controls - right aligned
    if isinstance(value, bool):
        value_text = "ON" if value else "OFF"
    else:
        value_text = str(value)

    # Calculate right-aligned position for the value
    value_width = text_width(value_text, 28)
    value_right_edge = x + 340  # Total row width
    value_x = value_right_edge - value_width

    draw_text(screen, value_text, value_x, y, text_color, 28)


def draw_menu(screen, params, cursor):
    screen.fill(BLACK)

    # Main title
    title = "Darwin"
    title_x = (screen.get_width() - text_width(title, 48)) / 2
    draw_text(screen, title, title_x, 20, WHITE, 48)

    # Subtitle
    subtitle = "Parameters Configuration"
    subtitle_x = (screen.get_width() - text_width(subtitle, 28)) / 2
    draw_text(screen, subtitle, subtitle_x, 120, GREY, 28)

    # Parameter list
    param_infos = get_parameter_info()
    y_offset = 160

    # Calculate center position for parameters with size 28 text
    # Row width: longest name (203) + gap to value (260-203=57) + value area (80) = 340
    row_width = 340  # Total width of parameter row with size 28 text
    center_x = (screen.get_width() - row_width) / 2

    for i, param_info in enumerate(param_infos):
        # Draw parameter row
        value = getattr(params, param_info["key"])
        is_selected = i == cursor

        draw_parameter_row(screen, param_info, value, center_x, y_offset, is_selected)
        y_offset += 50  # Reduced spacing since no descriptions

    # Control instructions
    instructions_y = y_offset + 80
    instructions = [
        "Navigation: UP/DOWN arrows or J/K to select",
        "Modify: LEFT/RIGHT arrows or H/L to change value",
        "Actions: [S] Save | [SPACE] Start | [Q] Exit",
    ]

    for i, instruction in enumerate(instructions):
        instr_x = (screen.get_width() - text_width(instruction, 28)) / 2
        draw_text(screen, instruction, instr_x, instructions_y + i * 20, GREY, 28)

    return param_infos


def adjust_param(params, param_info, direction):
    key = param_info["key"]
    val = getattr(params, key)

    if isinstance(val, bool):
        setattr(params, key, not val)
    elif isinstance(val, int):
        new_val = val + direction * param_info["step"]
        new_val = clamp(new_val, param_info["min"], param_info["max"])
        setattr(params, key, int(new_val))
    else:
        new_val = val + direction * param_info["step"]
        new_val = clamp(new_val, param_info["min"], param_info["max"])
        setattr(params, key, float(new_val))


def handle_menu_events(events, params, cursor, param_infos, key_repeat_delay):
    # Handle discrete events first
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                sys.exit(0)
            elif event.key == pg.K_SPACE:
                return cursor, False, key_repeat_delay  # Start simulation
            elif event.key == pg.K_s:
                save_params(params)

    # Handle held keys with timing control
    if key_repeat_delay <= 0:
        keys = pg.key.get_pressed()

        # Navigation
        if keys[pg.K_k] or keys[pg.K_UP]:
            cursor = max(0, cursor - 1)
            key_repeat_delay = 8
        elif keys[pg.K_j] or keys[pg.K_DOWN]:
            cursor = min(len(param_infos) - 1, cursor + 1)
            key_repeat_delay = 8

        # Parameter adjustment
        if keys[pg.K_h] or keys[pg.K_LEFT]:
            direction = -1
            param_info = param_infos[cursor]
            adjust_param(params, param_info, direction)
            key_repeat_delay = 4
        elif keys[pg.K_l] or keys[pg.K_RIGHT]:
            direction = 1
            param_info = param_infos[cursor]
            adjust_param(params, param_info, direction)
            key_repeat_delay = 4
    else:
        key_repeat_delay -= 1

    return cursor, True, key_repeat_delay


def show_menu_screen(screen, clock, params):
    """Display the menu screen with key holding support."""
    cursor = 0
    in_menu_screen = True
    key_repeat_delay = 0  # Timing control for key holding

    while in_menu_screen:
        param_infos = draw_menu(screen, params, cursor)

        pg.display.flip()
        cursor, in_menu_screen, key_repeat_delay = handle_menu_events(
            pg.event.get(), params, cursor, param_infos, key_repeat_delay
        )
        clock.tick(60)  # Higher framerate for smoother interactions
