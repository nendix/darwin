# ui/simulation_screen.py
import pygame as pg
from .common import draw_text
from .style import BLACK, BLUE, RED, GREEN, WHITE, GREY
from ..config import save_params
from ..utils import clamp
from ..simulation import World
from ..analytics import create_population_chart, create_fitness_chart


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

    draw_text(
        screen,
        f"Generation: {world.generation+1}/{params.generations}",
        20,
        20,
        WHITE,
        22,
    )
    draw_text(
        screen,
        f"Step: {world.time}/{params.steps_per_generation}",
        20,
        50,
        WHITE,
        22,
    )
    draw_text(
        screen,
        f"Prey: {len(world.preys)}  |  Predators: {len(world.predators)}",
        20,
        80,
        WHITE,
        22,
    )

    # Bottom controls with consistent styling
    controls_text = (
        f"Speed x{params.sim_speed} [+/-]  |  Vision [V]  |  Menu [M]  |  Exit [Q]"
    )
    controls_y = screen.get_height() - 30
    draw_text(
        screen,
        controls_text,
        20,
        controls_y,
        GREY,
        22,
    )


def handle_simulation_events(events, params):
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
                return "menu"
            elif event.key == pg.K_s:
                save_params(params)
            elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                params.sim_speed = clamp(params.sim_speed + 1, 1, 12)
            elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                params.sim_speed = clamp(params.sim_speed - 1, 1, 12)
    return True


def show_simulation_screen(screen, clock, params):
    world = World(params)
    world.reset_population()
    in_simulation_screen = True

    while in_simulation_screen:
        event_result = handle_simulation_events(pg.event.get(), params)

        if event_result == "menu":
            from .menu_screen import show_menu_screen

            show_menu_screen(screen, clock, params)
            return params
        elif not event_result:
            in_simulation_screen = False

        for _ in range(int(params.sim_speed)):
            world.step()
            if world.time >= params.steps_per_generation:
                world.end_generation()
                if world.generation + 1 >= params.generations:
                    in_simulation_screen = False
                    break
                world.new_generation()

        draw_world(screen, world, params)
        pg.display.flip()
        clock.tick(params.fps_limit)

    create_population_chart(world)
    create_fitness_chart(world)
    return params
