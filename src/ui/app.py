import pygame as pg

from ..config import load_params
from .menu_screen import run_menu
from .simulation_screen import run_simulation
from .final_screen import run_final_screen


def run_app():
    """Gestisce il ciclo completo: menu -> simulazione -> schermata finale"""
    pg.init()
    params = load_params()
    screen = pg.display.set_mode((params.world_w, params.world_h))
    pg.display.set_caption("Darwin")
    clock = pg.time.Clock()

    # Run menu
    run_menu(screen, clock, params)

    # Run simulation
    params = run_simulation(screen, clock, params)

    # Final screen
    run_final_screen(screen, params)

    pg.quit()
