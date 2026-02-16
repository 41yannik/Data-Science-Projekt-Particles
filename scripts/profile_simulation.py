"""
Benchmark der Particle Life Simulation: Vorher/Nachher-Vergleich (Issue #45).

Misst FPS und ms/step bei verschiedenen Partikelzahlen.
Ergebnisse werden in docs/benchmark_results.md gespeichert.
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import particle_life.config as config  # noqa: E402
from particle_life.physics import HAS_NUMBA  # noqa: E402
from particle_life.simulation import ParticleSystem  # noqa: E402

PARTICLE_COUNTS = [100, 500, 1000, 1500, 2000, 3000, 5000]
WARMUP_STEPS = 10
BENCH_STEPS = 50


def benchmark(n_particles: int) -> tuple[float, float, float]:
    """Benchmark für eine bestimmte Partikelzahl.

    Returns
    -------
    ms_per_step : float
    fps : float
    mem_mb : float – Geschätzter Speicher (nur Spatial Hash, nicht N×N)
    """
    np.random.seed(config.SEED)
    sim = ParticleSystem(n_particles=n_particles)

    # Warmup (inkl. Numba-JIT-Kompilierung beim ersten Aufruf)
    for _ in range(WARMUP_STEPS):
        sim.update(config.DT)

    t0 = time.perf_counter()
    for _ in range(BENCH_STEPS):
        sim.update(config.DT)
    elapsed = time.perf_counter() - t0

    ms = elapsed / BENCH_STEPS * 1000
    fps = 1000.0 / ms if ms > 0 else float("inf")

    # Speicher: Positions + Velocities + Types + total_force
    mem = (n_particles * 2 * 4 * 3 + n_particles * 4) / 1024 / 1024

    return ms, fps, mem


def main():
    backend = "Numba JIT + Spatial Hashing" if HAS_NUMBA else "NumPy + Spatial Hashing"
    print(f"=== Benchmark: {backend} ===\n")
    print(f"  {'Partikel':>8} | {'ms/step':>10} | {'FPS':>8} | {'Speicher':>10}")
    print(f"  {'-'*8}-+-{'-'*10}-+-{'-'*8}-+-{'-'*10}")

    results = []
    for n in PARTICLE_COUNTS:
        ms, fps, mem = benchmark(n)
        results.append((n, ms, fps, mem))
        print(f"  {n:>8} | {ms:>10.2f} | {fps:>8.1f} | {mem:>7.3f} MB")

    # --- Report speichern ---
    report_path = (
        Path(__file__).resolve().parent.parent / "docs" / "benchmark_results.md"
    )
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w") as f:
        f.write("# Benchmark-Ergebnisse: Performance-Optimierung (Issue #45)\n\n")
        f.write(f"**Backend:** {backend}\n\n")
        f.write("| Partikel | ms/step | FPS | Speicher |\n")
        f.write("|----------|---------|-----|----------|\n")
        for n, ms, fps, mem in results:
            f.write(f"| {n} | {ms:.2f} | {fps:.1f} | {mem:.3f} MB |\n")
        f.write("\n## Optimierung\n\n")
        f.write(
            "- **Spatial Hashing:** Grid-basierte Nachbarschaftssuche "
            "(O(n) statt O(n²))\n"
        )
        f.write(
            "- **Numba JIT:** Innere Berechnungsschleife mit "
            "`@njit(parallel=True)` kompiliert\n"
        )
        f.write(
            "- **Speicher:** Keine N×N Arrays mehr – nur O(n) Speicher "
            "für Partikel-Daten\n"
        )

    print(f"\n✅ Report: {report_path}")


if __name__ == "__main__":
    main()
