"""
Pygame viewer FPS test with new physics engine.
Measures FPS for different particle counts (5 sec per test).
"""

import sys
import time
from pathlib import Path

import numpy as np
import pygame

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import particle_life.config as config
from particle_life.simulation import ParticleSystem


def test_pygame_fps(n_particles: int, duration: float = 5.0) -> float:
    """Start Pygame, render n_particles for duration seconds, return FPS."""
    np.random.seed(config.SEED)
    sim = ParticleSystem(n_particles=n_particles)

    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(f"FPS-Test: {n_particles} Partikel")
    clock = pygame.time.Clock()

    colors = [pygame.Color(*c) for c in config.COLOR_PALETTE]

    frames = 0
    start = time.perf_counter()

    while time.perf_counter() - start < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0.0

        sim.update(config.DT)

        screen.fill(config.BACKGROUND_COLOR)
        positions = sim.get_positions()
        types = sim.get_types()
        for i in range(len(positions)):
            x, y = int(positions[i, 0]), int(positions[i, 1])
            pygame.draw.circle(screen, colors[types[i]], (x, y), 2)

        pygame.display.flip()
        clock.tick(0)  # kein FPS-Limit
        frames += 1

    elapsed = time.perf_counter() - start
    pygame.quit()
    return frames / elapsed


print("=== Pygame FPS-Test ===\n")
print(f"  {'Partikel':>8} | {'FPS':>8}")
print(f"  {'-'*8}-+-{'-'*8}")

results = []
for n in [1000, 2000, 3000, 5000]:
    fps = test_pygame_fps(n, duration=5.0)
    results.append((n, fps))
    print(f"  {n:>8} | {fps:>8.1f}")

print("\nFertig!")
