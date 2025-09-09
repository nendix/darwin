import pygame

from darwin import config as c

class Food:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.available = True
        self.energy_value = c.FOOD_ENERGY_GAIN

    def draw(self, screen: pygame.Surface):
        screen_x = int(self.x)
        screen_y = int(self.y)

        if 0 <= screen_x <= c.SCREEN_WIDTH and 0 <= screen_y <= c.SCREEN_HEIGHT:
            pygame.draw.circle(screen, c.GREEN, (screen_x, screen_y), c.FOOD_RADIUS)

    def update(self, dt, entities_nearby=None):
        pass
