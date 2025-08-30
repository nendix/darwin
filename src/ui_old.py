import pygame as pg
import sys
from pathlib import Path

from .plotter import make_plots
from .config import load_params, save_params
from .simulation import World
from .utils import clamp

# Colors
BLACK = (10, 10, 10)
BLUE = (120, 180, 255)  # blu chiaro
RED = (220, 70, 70)  # rosso
GREEN = (70, 200, 120)  # verde chiaro
WHITE = (240, 240, 240)
GREY = (120, 120, 120)
YELLOW = (255, 200, 80)

FONT_NAME = None  # default font


def draw_text(surf, txt, x, y, color=WHITE, size=16):
    font = pg.font.Font(FONT_NAME, size)
    surf.blit(font.render(txt, True, color), (x, y))


def text_width(txt, size=16):
    font = pg.font.Font(FONT_NAME, size)
    width, _ = font.size(txt)
    return width


def draw_world(screen, world, params):
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


def draw_menu(screen, params, cursor):
    screen.fill((12, 12, 12))

    # Titolo centrato
    txt = "DARWIN - Parametri (J/K seleziona, H/L modifica, S salva, SPACE avvia)"
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 24)) / 2, 12, WHITE, 24
    )

    # Entries
    entries = [
        ("population_prey", params.population_prey, 4, 300, 1),
        ("population_pred", params.population_pred, 2, 100, 1),
        ("food_count", params.food_count, 0, 900, 1),
        ("generations", params.generations, 1, 100, 1),
        ("draw_vision", params.draw_vision, 0, 1, 1),
        ("sim_speed", params.sim_speed, 1, 10, 1),
    ]
    y = 80
    for i, (k, val, lo, hi, step) in enumerate(entries):
        display = val if not isinstance(val, bool) else ("ON" if val else "OFF")
        line = f"{k:>20}: {display}"

        if i == cursor:
            draw_text(
                screen,
                line,
                (screen.get_width() - text_width(line, 32)) / 2,
                y + i * 32,
                YELLOW,
                32,
            )
        else:
            draw_text(
                screen,
                line,
                (screen.get_width() - text_width(line, 28)) / 2,
                y + i * 32,
                WHITE,
                28,
            )

    txt = "Start [SPACE] | Exit [Q]"
    draw_text(
        screen,
        txt,
        (screen.get_width() - text_width(txt, 24)) / 2,
        y + len(entries) * 32 + 20,
        GREY,
        24,
    )

    return entries


def adjust_param(params, key, lo, hi, step, direction):
    val = getattr(params, key)
    if isinstance(val, bool):
        setattr(params, key, not val)
    elif isinstance(val, int):
        setattr(params, key, int(clamp(val + direction * step, lo, hi)))
    else:
        setattr(params, key, float(clamp(val + direction * step, lo, hi)))


def handle_menu_events(events, params, cursor, entries):
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                pg.quit()
                sys.exit(0)
            if event.key == pg.K_SPACE:
                return cursor, False
            if event.key == pg.K_s:
                save_params(params)
            if event.key == pg.K_k:
                cursor = max(0, cursor - 1)
            if event.key == pg.K_j:
                cursor = min(len(entries) - 1, cursor + 1)
            if event.key in (pg.K_h, pg.K_l):
                direction = -1 if event.key == pg.K_h else 1
                k, v, lo, hi, step = entries[cursor]
                adjust_param(params, k, lo, hi, step, direction)
    return cursor, True


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
                run_app()
            elif event.key == pg.K_s:
                save_params(params)
            elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                params.sim_speed = clamp(params.sim_speed + 1, 1, 10)
            elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                params.sim_speed = clamp(params.sim_speed - 1, 1, 10)
    return True


def show_menu_screen(screen, clock, params):
    cursor = 0
    in_menu = True
    while in_menu:
        entries = draw_menu(screen, params, cursor)
        pg.display.flip()
        cursor, in_menu = handle_menu_events(pg.event.get(), params, cursor, entries)
        clock.tick(30)


def show_simulation_screen(screen, clock, params):
    world = World(params)
    world.reset_population()
    running = True
    while running:
        if not handle_simulation_events(pg.event.get(), params):
            running = False

        for _ in range(int(params.sim_speed)):
            world.step()
            if world.time >= params.steps_per_generation:
                world.end_generation()
                if world.generation + 1 >= params.generations:
                    running = False
                    break
                world.new_generation()

        draw_world(screen, world, params)
        pg.display.flip()
        clock.tick(params.fps_limit)

    make_plots(world)
    return params


def run_app():
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
    screen.fill(BLACK)
    out_dir = Path("output")
    txt = "Simulation ended."
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 72)) / 2, 40, WHITE, 72
    )
    txt = f"Graphs saved in {out_dir}/"
    draw_text(screen, txt, (screen.get_width() - text_width(txt, 36)) / 2, 80, GREY, 36)
    txt = "Exit [Q] | Menu [M]"
    draw_text(
        screen, txt, (screen.get_width() - text_width(txt, 36)) / 2, 110, GREY, 36
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
                    run_app()
        pg.time.wait(50)

    pg.quit()
