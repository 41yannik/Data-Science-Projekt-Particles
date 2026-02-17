"""
Direct comparison: O(n2) brute force vs. spatial hashing + Numba.
Runs both engines with the same initial conditions.
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import particle_life.config as config
from particle_life.legacy.physics_bruteforce import PhysicsEngine as BruteForceEngine
from particle_life.physics import PhysicsEngine as OptimizedEngine
from particle_life.simulation import ParticleSystem

# Numba JIT warmup (compile once)
print("Numba JIT Warmup...", end=" ", flush=True)
np.random.seed(config.SEED)
warmup_sim = ParticleSystem(n_particles=50)
warmup_engine = OptimizedEngine(50)
for _ in range(5):
    warmup_engine.step(warmup_sim, config.DT)
print("fertig.\n")


def bench(engine_cls, n_particles, n_steps=30):
    """Measure ms/step for an engine."""
    np.random.seed(config.SEED)
    sim = ParticleSystem(n_particles=n_particles)
    engine = engine_cls(n_particles)

    # Warmup (Numba is already compiled now)
    for _ in range(5):
        engine.step(sim, config.DT)

    start = time.perf_counter()
    for _ in range(n_steps):
        engine.step(sim, config.DT)
    elapsed = time.perf_counter() - start

    ms = elapsed / n_steps * 1000
    return ms


print("=" * 65)
print("  Vergleich: Brute-Force O(n2) vs. Spatial Hashing O(n)")
print("=" * 65)
print()
print(f"  {'Partikel':>8} | {'Brute-Force':>14} | {'Optimiert':>14} | {'Speedup':>8}")
print(f"  {'-'*8}-+-{'-'*14}-+-{'-'*14}-+-{'-'*8}")

for n in [100, 500, 1000, 1500, 2000, 3000]:
    ms_old = bench(BruteForceEngine, n)
    ms_new = bench(OptimizedEngine, n)
    speedup = ms_old / ms_new if ms_new > 0 else float("inf")
    print(f"  {n:>8} | {ms_old:>10.2f} ms | {ms_new:>10.2f} ms | {speedup:>7.1f}x")

print("\nFertig!")
