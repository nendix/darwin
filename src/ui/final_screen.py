import pygame as pg
from pathlib import Path
from .common import draw_text, text_width
from .style import BLACK, WHITE, GREY
from ..config import save_params
from .menu_screen import show_menu_screen


def show_final_screen(screen, params):
    screen.fill(BLACK)
    out_dir = Path("output")

    # Titolo
    txt = "Simulation ended."
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 72)) / 2, 40, WHITE, 72
    )

    # Sottotitolo
    txt = f"Graphs saved in {out_dir}/"
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 36)) / 2, 100, GREY, 36
    )

    # Footer
    txt = "Exit [Q] | Menu [M]"
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 36)) / 2, 160, GREY, 36
    )

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
