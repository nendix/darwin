import pygame as pg
from darwin import config as c

def draw_text(surf, txt, x, y, color=c.WHITE, size=16):
    font = pg.font.Font(c.FONT_NAME, size)
    surf.blit(font.render(txt, True, color), (x, y))

def text_width(txt, size=16):
    font = pg.font.Font(c.FONT_NAME, size)
    width, _ = font.size(txt)
    return width
