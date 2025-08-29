import pygame as pg
from pathlib import Path
import matplotlib.pyplot as plt

from .config import load_params, save_params
from .simulation import World
from .utils import clamp

WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
GREY = (70, 70, 70)
RED = (220, 70, 70)
BLUE = (120, 180, 255)
GREEN = (70, 200, 120)
YELLOW = (250, 220, 100)

FONT_NAME = "freesansbold.ttf"


def draw_text(surf, txt, x, y, color=WHITE, size=16):
    font = pg.font.Font(FONT_NAME, size)
    t = font.render(txt, True, color)
    surf.blit(t, (x, y))


def draw_world(screen, world, params):
    screen.fill((22, 22, 26))
    # foods
    for f in world.foods:
        pg.draw.circle(screen, GREEN, (int(f.pos[0]), int(f.pos[1])), 3)

    # preys
    for p in world.preys:
        for p in world.preys:
            pg.draw.circle(screen, BLUE, (int(p.x), int(p.y)), 5)
            if params.draw_vision:
                pg.draw.circle(screen, BLUE, (int(p.x), int(p.y)), int(p.dna.vision), 1)

    # predators
    for pr in world.predators:
        pg.draw.circle(screen, RED, (int(pr.x), int(pr.y)), 6)
        if params.draw_vision:
            pg.draw.circle(screen, RED, (int(pr.x), int(pr.y)), int(pr.dna.vision), 1)

    # HUD
    draw_text(
        screen,
        f"Gen {world.generation+1}/{params.generations}  t:{world.time}/{params.steps_per_generation}",
        10,
        8,
        WHITE,
        16,
    )
    draw_text(
        screen,
        f"Prede: {len(world.preys)}  Predatori: {len(world.predators)}",
        10,
        28,
        WHITE,
        16,
    )
    draw_text(
        screen,
        f"Speed x{params.sim_speed}  [ +/- ]  |  Visione [V]  |  Salva param [S]  |  Menu [M]  |  Quit [ESC]",
        10,
        48,
        GREY,
        14,
    )


def draw_menu(screen, params, cursor):
    screen.fill((18, 18, 22))
    draw_text(
        screen,
        "DARWIN - Parametri (J/K per scorrere, H/L per modificare, S per salvare, Invio per avviare)",
        20,
        20,
        WHITE,
        16,
    )
    vals = [
        ("population_prey", params.population_prey, 10, 200, 1),
        ("population_pred", params.population_pred, 4, 80, 1),
        ("food_count", params.food_count, 10, 200, 2),
        ("steps_per_generation", params.steps_per_generation, 600, 8000, 50),
        ("generations", params.generations, 5, 200, 1),
        ("elitism", params.elitism, 0, 10, 1),
        ("mutation_rate", params.mutation_rate, 0.0, 0.8, 0.01),
        ("mutation_std", params.mutation_std, 0.01, 0.6, 0.01),
        ("crossover_rate", params.crossover_rate, 0.0, 1.0, 0.05),
        ("tournament_k", params.tournament_k, 2, 8, 1),
        ("draw_vision", params.draw_vision, 0, 1, 1),
    ]
    start_y = 70
    for i, (k, val, lo, hi, step) in enumerate(vals):
        sel = ">>" if i == cursor else "  "
        display_val = val
        if isinstance(val, bool):
            display_val = "ON" if val else "OFF"
        draw_text(
            screen,
            f"{sel} {k:>20}: {display_val}",
            40,
            start_y + i * 26,
            YELLOW if i == cursor else WHITE,
            16,
        )
    draw_text(
        screen,
        "[Invio] Avvia  |  [ESC] Esci",
        40,
        start_y + len(vals) * 26 + 20,
        GREY,
        14,
    )
    return vals


def adjust_param(params, key, lo, hi, step, direction):
    val = getattr(params, key)
    if isinstance(val, bool):
        setattr(params, key, not val)
        return
    if isinstance(val, int):
        val += direction * step
        val = int(clamp(val, lo, hi))
    else:
        val += direction * step
        val = float(clamp(val, lo, hi))
    setattr(params, key, val)


def make_plots(world: World):
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    gens = [s.generation + 1 for s in world.history]
    prey_pop = [s.prey_pop for s in world.history]
    pred_pop = [s.pred_pop for s in world.history]
    prey_fit = [s.prey_fitness_avg for s in world.history]
    pred_fit = [s.pred_fitness_avg for s in world.history]

    plt.figure(figsize=(8, 4.2))
    plt.plot(gens, prey_pop, label="Prede")
    plt.plot(gens, pred_pop, label="Predatori")
    plt.xlabel("Generazione")
    plt.ylabel("Popolazione")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "populations.png", dpi=140)
    plt.close()

    plt.figure(figsize=(8, 4.2))
    plt.plot(gens, prey_fit, label="Prey fitness media")
    plt.plot(gens, pred_fit, label="Predator fitness media")
    plt.xlabel("Generazione")
    plt.ylabel("Fitness media")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "fitness.png", dpi=140)
    plt.close()


def run_with_pygame():
    pg.init()
    pg.display.set_caption("Darwin - Predator & Prey GA")
    params = load_params()

    # Menu loop
    screen = pg.display.set_mode((params.world_w, params.world_h))
    clock = pg.time.Clock()

    cursor = 0
    in_menu = True
    while in_menu:
        vals = draw_menu(screen, params, cursor)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return 0
                if event.key == pg.K_RETURN:
                    in_menu = False
                if event.key == pg.K_s:
                    save_params(params)
                if event.key == pg.K_k:
                    cursor = max(0, cursor - 1)
                if event.key == pg.K_j:
                    cursor = min(len(vals) - 1, cursor + 1)
                if event.key in (pg.K_h, pg.K_l):
                    direction = -1 if event.key == pg.K_h else 1
                    k, v, lo, hi, step = vals[cursor]
                    adjust_param(params, k, lo, hi, step, direction)

        clock.tick(30)

    # Simulation
    world = World(params=params)
    world.reset_population()
    running = True

    while running:
        # Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_v:
                    params.draw_vision = not params.draw_vision
                elif event.key == pg.K_m:
                    # back to menu: save and restart
                    save_params(params)
                    return run_with_pygame()
                elif event.key == pg.K_s:
                    save_params(params)
                elif event.key in (
                    pg.K_PLUS,
                    pg.K_EQUALS,
                ):  # '+' can be '=' on some layouts
                    params.sim_speed = clamp(params.sim_speed + 1, 1, 8)
                elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                    params.sim_speed = clamp(params.sim_speed - 1, 1, 8)

        # Steps
        for _ in range(int(params.sim_speed)):
            world.step()
            if world.time >= params.steps_per_generation:
                world.end_generation()
                if world.generation + 1 >= params.generations:
                    running = False
                    break
                world.new_generation()

        # Draw
        draw_world(screen, world, params)
        pg.display.flip()
        clock.tick(params.fps_limit)

    # After sim -> plots
    make_plots(world)

    # small end screen
    screen.fill((15, 15, 18))
    from pathlib import Path

    p1 = Path("output") / "populations.png"
    p2 = Path("output") / "fitness.png"
    draw_text(screen, "Simulazione terminata.", 40, 40, WHITE, 22)
    draw_text(screen, f"Grafici salvati in {p1} e {p2}", 40, 80, GREY, 16)
    draw_text(screen, "Premi ESC per uscire.", 40, 110, GREY, 16)
    pg.display.flip()

    # wait ESC
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                waiting = False
        pg.time.wait(50)

    pg.quit()
    return 0
