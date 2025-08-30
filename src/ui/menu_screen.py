import pygame as pg
import sys
from .common import draw_text, text_width
from .style import WHITE, GREY, YELLOW
from ..config import save_params
from ..utils import clamp


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

        color = YELLOW if i == cursor else WHITE
        size = 32 if i == cursor else 28

        draw_text(
            screen,
            line,
            (screen.get_width() - text_width(line, size)) / 2,
            y + i * 32,
            color,
            size,
        )

    # Footer
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


def run_menu(screen, clock, params):
    cursor = 0
    in_menu = True
    while in_menu:
        entries = draw_menu(screen, params, cursor)
        pg.display.flip()
        cursor, in_menu = handle_menu_events(pg.event.get(), params, cursor, entries)
        clock.tick(30)
