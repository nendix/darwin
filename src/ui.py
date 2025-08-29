import pygame as pg
import sys
from pathlib import Path
import matplotlib.pyplot as plt

from .config import load_params, save_params
from .simulation import World
from .utils import clamp

# Colors
BG = (10, 10, 10)
PREY_COLOR = (120, 180, 255)  # blu chiaro
PRED_COLOR = (220, 70, 70)  # rosso
FOOD_COLOR = (70, 200, 120)  # verde chiaro
WHITE = (240, 240, 240)
GREY = (120, 120, 120)

FONT_NAME = None  # default font


def draw_text(surf, txt, x, y, color=WHITE, size=16):
    font = pg.font.Font(FONT_NAME, size)
    surf.blit(font.render(txt, True, color), (x, y))


def draw_world(screen, world, params):
    screen.fill(BG)
    # foods
    for f in world.foods:
        pg.draw.circle(screen, FOOD_COLOR, (int(f.pos[0]), int(f.pos[1])), 4)

    # preys
    for p in world.preys:
        pg.draw.circle(screen, PREY_COLOR, (int(p.x), int(p.y)), 5)
        if params.draw_vision:
            pg.draw.circle(
                screen, (100, 150, 255), (int(p.x), int(p.y)), int(p.dna.vision), 1
            )

    # predators
    for pr in world.predators:
        pg.draw.circle(screen, PRED_COLOR, (int(pr.x), int(pr.y)), 6)
        if params.draw_vision:
            pg.draw.circle(
                screen, (180, 80, 80), (int(pr.x), int(pr.y)), int(pr.dna.vision), 1
            )

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
        f"Prede: {len(world.preys)}  Predatori: {len(world.predators)}  Cibo: {len(world.foods)}",
        10,
        28,
        WHITE,
        16,
    )
    draw_text(
        screen,
        f"Speed x{params.sim_speed}  [+/-]  |  Visione [V]  |  Menu [M]  |  ESC esci",
        10,
        48,
        GREY,
        14,
    )


def draw_menu(screen, params, cursor):
    screen.fill((12, 12, 12))
    draw_text(
        screen,
        "DARWIN - Parametri (↑↓ seleziona, ←→ modifica, S salva, Invio avvia)",
        18,
        14,
        WHITE,
        16,
    )
    entries = [
        ("population_prey", params.population_prey, 4, 200, 1),
        ("population_pred", params.population_pred, 2, 100, 1),
        ("food_count", params.food_count, 0, 300, 1),
        ("steps_per_generation", params.steps_per_generation, 200, 20000, 100),
        ("generations", params.generations, 1, 500, 1),
        ("draw_vision", params.draw_vision, 0, 1, 1),
        ("sim_speed", params.sim_speed, 1, 8, 1),
    ]
    y = 60
    for i, (k, val, lo, hi, step) in enumerate(entries):
        sel = ">>" if i == cursor else "  "
        display = val
        if isinstance(val, bool):
            display = "ON" if val else "OFF"
        draw_text(
            screen,
            f"{sel} {k:>20}: {display}",
            40,
            y + i * 28,
            (255, 200, 80) if i == cursor else WHITE,
            18,
        )
    draw_text(
        screen, "[Invio] Avvia  |  [ESC] Esci", 40, y + len(entries) * 28 + 12, GREY, 14
    )
    return entries


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
    plt.plot(gens, prey_pop, label="Prede", color=(0.47, 0.7, 1.0))
    plt.plot(gens, pred_pop, label="Predatori", color=(0.86, 0.27, 0.27))
    plt.xlabel("Generazione")
    plt.ylabel("Popolazione")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "populations.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4.2))
    plt.plot(gens, prey_fit, label="Prey fitness media", color=(0.47, 0.7, 1.0))
    plt.plot(gens, pred_fit, label="Predator fitness media", color=(0.86, 0.27, 0.27))
    plt.xlabel("Generazione")
    plt.ylabel("Fitness media")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "fitness.png", dpi=150)
    plt.close()


def run_app():
    pg.init()
    params = load_params()
    screen = pg.display.set_mode((params.world_w, params.world_h))
    pg.display.set_caption("Darwin - Predator & Prey GA")
    clock = pg.time.Clock()

    # Menu
    cursor = 0
    in_menu = True
    while in_menu:
        entries = draw_menu(screen, params, cursor)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)
                if event.key == pg.K_RETURN:
                    in_menu = False
                if event.key == pg.K_s:
                    save_params(params)
                if event.key == pg.K_UP:
                    cursor = max(0, cursor - 1)
                if event.key == pg.K_DOWN:
                    cursor = min(len(entries) - 1, cursor + 1)
                if event.key in (pg.K_LEFT, pg.K_RIGHT):
                    direction = -1 if event.key == pg.K_LEFT else 1
                    k, v, lo, hi, step = entries[cursor]
                    adjust_param(params, k, lo, hi, step, direction)
        clock.tick(30)

    # Simulation start
    world = World(params)
    world.reset_population()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_v:
                    params.draw_vision = not params.draw_vision
                elif event.key == pg.K_m:
                    save_params(params)
                    return run_app()
                elif event.key == pg.K_s:
                    save_params(params)
                elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                    params.sim_speed = clamp(params.sim_speed + 1, 1, 8)
                elif event.key in (pg.K_MINUS, pg.K_UNDERSCORE):
                    params.sim_speed = clamp(params.sim_speed - 1, 1, 8)

        # advance steps
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

    # finished
    make_plots(world)

    # final screen
    screen.fill(BG)
    out_dir = Path("output")
    draw_text(screen, "Simulazione terminata.", 40, 40, WHITE, 22)
    draw_text(screen, f"Grafici salvati in {out_dir}/", 40, 80, GREY, 16)
    draw_text(
        screen, "Premi ESC per uscire o M per tornare al menu.", 40, 110, GREY, 16
    )
    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    waiting = False
                if event.key == pg.K_m:
                    save_params(params)
                    return run_app()
        pg.time.wait(50)

    pg.quit()
