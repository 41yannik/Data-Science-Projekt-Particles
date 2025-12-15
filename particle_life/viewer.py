import sys

import numpy as np
import pygame

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
    paused = False
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_f:
                    sim.friction = float(min(max(sim.friction + 0.01, 0.0), 1.0))
                elif event.key == pygame.K_g:
                    sim.friction = float(min(max(sim.friction - 0.01, 0.0), 1.0))
                elif event.key == pygame.K_r:
                    config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 1.1, 0.0))
                elif event.key == pygame.K_e:
                    config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 0.9, 0.0))
                elif event.key == pygame.K_t:
                    config.MAX_RADIUS = float(max(config.MAX_RADIUS + 1.0, 0.0))
                elif event.key == pygame.K_z:
                    config.MAX_RADIUS = float(max(config.MAX_RADIUS - 1.0, 0.0))

        if not paused:
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
        mode_text = "paused" if paused else "running"
        info = (
            f"step={step} fps={fps:.1f} "
            f"friction={sim.friction:.3f} "
            f"force={config.FORCE_FACTOR:.2f} "
            f"radius={config.MAX_RADIUS:.1f} "
            f"mode={mode_text}"
        )
        text_surface = font.render(info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        step += 1

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
