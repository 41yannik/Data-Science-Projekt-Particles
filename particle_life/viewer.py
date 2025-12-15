import sys

import pygame
import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem


def run() -> None:
    if config.SEED is not None:
        np.random.seed(config.SEED)

    pygame.init()
    screen = pygame.display.set_mode(
        (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    )
    pygame.display.set_caption(config.TITLE)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    sim = ParticleSystem()
    running = True
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        sim.update(config.DT)
        positions = sim.get_positions()
        types = sim.get_types()

        screen.fill(config.BACKGROUND_COLOR)

        radius = 2
        for i in range(len(positions)):
            x = int(positions[i, 0])
            y = int(positions[i, 1])
            t = int(types[i])
            color_index = t % len(config.COLOR_PALETTE)
            color = config.COLOR_PALETTE[color_index]
            pygame.draw.circle(screen, color, (x, y), radius)

        fps = clock.get_fps()
        info = f"step={step} fps={fps:.1f}"
        text_surface = font.render(info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        step += 1

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()

