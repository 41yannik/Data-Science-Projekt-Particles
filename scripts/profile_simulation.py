"""
Profiling der Particle Life Simulation mit cProfile und timeit.
Ergebnisse werden in docs/profiling_report.md gespeichert.
"""

import cProfile
import pstats
import sys
import time
import timeit
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import particle_life.config as config
from particle_life.simulation import ParticleSystem

# --- cProfile ---
print("=== cProfile (1000 Partikel, 100 Steps) ===\n")
np.random.seed(config.SEED)
sim = ParticleSystem(n_particles=1000)

cProfile.run("[sim.update(config.DT) for _ in range(100)]", sort="cumulative")

# --- timeit ---
print("\n=== timeit Benchmarks ===\n")
np.random.seed(config.SEED)
sim = ParticleSystem(n_particles=1000)

ms = timeit.timeit(lambda: sim.update(config.DT), number=50) / 50 * 1000
print(f"  PhysicsEngine.step():  {ms:.2f} ms/step")

# --- Skalierung ---
print("\n=== Skalierung ===\n")
print(f"  {'Partikel':>8} | {'ms/step':>8} | {'FPS':>8} | {'Speicher':>10}")
print(f"  {'-'*8}-+-{'-'*8}-+-{'-'*8}-+-{'-'*10}")

results = []
for n in [100, 500, 1000, 1500, 2000, 3000]:
    np.random.seed(config.SEED)
    s = ParticleSystem(n_particles=n)
    for _ in range(5):  # warmup
        s.update(config.DT)

    t0 = time.perf_counter()
    for _ in range(30):
        s.update(config.DT)
    ms = (time.perf_counter() - t0) / 30 * 1000
    fps = 1000 / ms
    mem = n * n * 2 * 4 / 1024 / 1024

    results.append((n, ms, fps, mem))
    print(f"  {n:>8} | {ms:>8.2f} | {fps:>8.1f} | {mem:>7.1f} MB")

# --- Report speichern ---
report_path = Path(__file__).resolve().parent.parent / "docs" / "profiling_report.md"
report_path.parent.mkdir(exist_ok=True)

with open(report_path, "w") as f:
    f.write("# Profiling Report\n\n")
    f.write("| Partikel | ms/step | FPS | Speicher |\n")
    f.write("|----------|---------|-----|----------|\n")
    for n, ms, fps, mem in results:
        f.write(f"| {n} | {ms:.2f} | {fps:.1f} | {mem:.1f} MB |\n")
    f.write("\n**Bottleneck:** `PhysicsEngine.step()` ist O(n²) — "
            "das N×N Displacement-Array dominiert Rechenzeit und Speicher.\n")

print(f"\n✅ Report: {report_path}")
