import pygame as pg
from ..config import FONT_NAME, WHITE


def draw_text(surf, txt, x, y, color=WHITE, size=16):
    font = pg.font.Font(FONT_NAME, size)
    surf.blit(font.render(txt, True, color), (x, y))


def text_width(txt, size=16):
    font = pg.font.Font(FONT_NAME, size)
    width, _ = font.size(txt)
    return width
