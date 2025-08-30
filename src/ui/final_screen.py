import pygame as pg
from pathlib import Path
from .common import draw_text, text_width
from .style import BLACK, WHITE, GREY
from ..config import save_params
from .menu_screen import show_menu_screen


def show_final_screen(screen, params):
    screen.fill(BLACK)  # Match menu screen dark background
    out_dir = Path("output")

    # Calculate vertical centering
    screen_height = screen.get_height()
    total_text_height = (
        48 + 40 + 24 + 40 + 24
    )  # subtitle + gap + info + gap + instructions
    start_y = (screen_height - total_text_height) / 2

    # Subtitle
    subtitle = "Simulation Complete"
    subtitle_x = (screen.get_width() - text_width(subtitle, 48)) / 2
    draw_text(screen, subtitle, subtitle_x, start_y, WHITE, 48)

    # Information text
    info_text = f"Graphs saved in {out_dir}/"
    info_x = (screen.get_width() - text_width(info_text, 24)) / 2
    draw_text(screen, info_text, info_x, start_y + 68, GREY, 24)

    # Control instructions - match menu screen style
    instructions_y = start_y + 108
    instructions = [
        "Actions: [M] Return to Menu | [Q] Exit",
    ]

    for i, instruction in enumerate(instructions):
        instr_x = (screen.get_width() - text_width(instruction, 24)) / 2
        draw_text(screen, instruction, instr_x, instructions_y + i * 30, GREY, 24)

    pg.display.flip()

    in_final_screen = True
    while in_final_screen:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                in_final_screen = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    in_final_screen = False
                if event.key == pg.K_m:
                    save_params(params)
                    show_menu_screen(screen, pg.time.Clock(), params)
        pg.time.wait(50)

    pg.quit()
