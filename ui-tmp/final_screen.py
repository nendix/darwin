import pygame as pg
from pathlib import Path
from .common import draw_text, text_width
from .style import BLACK, WHITE, GREY
from ..config import save_params
from .menu_screen import run_menu


def run_final_screen(screen, params):
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

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    waiting = False
                if event.key == pg.K_m:
                    save_params(params)
                    run_menu(screen, pg.time.Clock(), params)
        pg.time.wait(50)

    pg.quit()
