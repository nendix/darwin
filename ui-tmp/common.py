import pygame as pg
from .style import FONT_NAME, WHITE


def draw_text(surf, txt, x, y, color=WHITE, size=16):
    font = pg.font.Font(FONT_NAME, size)
    surf.blit(font.render(txt, True, color), (x, y))


def text_width(txt, size=16):
    """Ritorna la larghezza di una stringa renderizzata con font e size."""
    font = pg.font.Font(FONT_NAME, size)
    width, _ = font.size(txt)
    return width
