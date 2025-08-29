# ui/simulation_screen.py
import pygame as pg
from .common import draw_text
from .style import BLACK, BLUE, RED, GREEN, WHITE, GREY
from ..config import save_params
from .menu_screen import run_menu
from ..utils import clamp


def draw_world(screen, world, params):
    """Disegna lo stato corrente del mondo (cibo, prede, predatori, HUD)."""
    screen.fill(BLACK)

    # foods
    for f in world.foods:
        pg.draw.circle(screen, GREEN, (int(f.pos[0]), int(f.pos[1])), 4)

    # preys
    for p in world.preys:
        pg.draw.circle(screen, BLUE, (int(p.x), int(p.y)), 5)
        if params.draw_vision:
            pg.draw.circle(
                screen, (100, 150, 255), (int(p.x), int(p.y)), int(p.dna.vision), 1
            )

    # predators
    for pr in world.predators:
        pg.draw.circle(screen, RED, (int(pr.x), int(pr.y)), 6)
        if params.draw_vision:
            pg.draw.circle(
                screen, (180, 80, 80), (int(pr.x), int(pr.y)), int(pr.dna.vision), 1
            )

    # HUD
    draw_text(
        screen,
        f"Gen {world.generation+1}/{params.generations}  t:{world.time}/{params.steps_per_generation}",
        12,
        8,
        WHITE,
        16,
    )
    draw_text(
        screen,
        f"Prede: {len(world.preys)}  Predatori: {len(world.predators)}",
        12,
        28,
        WHITE,
        16,
    )
    draw_text(
        screen,
        f"Speed x{params.sim_speed}  [+/-]  |  Vision [V]  |  Menu [M]  |  Exit [Q] ",
        12,
        48,
        GREY,
        16,
    )


def handle_simulation_events(events, params):
    """Gestisce input utente durante la simulazione."""
    for event in events:
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                return False
            elif event.key == pg.K_v:
                params.draw_vision = not params.draw_vision
            elif event.key == pg.K_m:
                save_params(params)
                run_menu(
                    screen=pg.display.get_surface(),
                    clock=pg.time.Clock(),
                    params=params,
                )
            elif event.key == pg.K_s:
                save_params(params)
            elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                params.sim_speed = clamp(params.sim_speed + 1, 1, 10)
            elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                params.sim_speed = clamp(params.sim_speed - 1, 1, 10)
    return True
