import pygame as pg

from ..config import load_params
from .menu_screen import show_menu_screen
from .simulation_screen import show_simulation_screen
from .final_screen import show_final_screen


def run_app():
    """Gestisce il ciclo completo: menu -> simulazione -> schermata finale"""
    pg.init()
    params = load_params()
    screen = pg.display.set_mode((params.world_w, params.world_h))
    pg.display.set_caption("Darwin")
    clock = pg.time.Clock()

    # Run menu
    show_menu_screen(screen, clock, params)

    # Run simulation
    params = show_simulation_screen(screen, clock, params)

    # Final screen
    show_final_screen(screen, params)

    pg.quit()
