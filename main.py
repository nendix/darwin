import pygame
import sys
from simulation import Simulation
from settings import Settings


def main():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Darwin - Predatore vs Preda")

    simulation = Simulation(settings, screen)
    clock = pygame.time.Clock()

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    simulation = Simulation(settings, screen)

        if not paused:
            simulation.update()

        simulation.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
