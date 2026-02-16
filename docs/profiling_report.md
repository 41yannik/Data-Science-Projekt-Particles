# Profiling Report: Vorher/Nachher-Vergleich

## Baseline — O(n²) Brute-Force (vor Optimierung)

Gemessen mit `scripts/profile_simulation.py` (cProfile + timeit).

| Partikel | ms/step | FPS | Speicher (N×N×2) |
|----------|---------|-----|------------------|
| 100 | 0.25 | 4000 | 0.1 MB |
| 500 | 5.60 | 179 | 1.9 MB |
| 1000 | 22.74 | 44 | 7.6 MB |
| 1500 | 50.76 | 20 | 17.2 MB |
| 2000 | 90.42 | 11 | 30.5 MB |
| 3000 | 185.11 | 5 | 68.7 MB |

**Bottleneck:** `PhysicsEngine.step()` mit O(n²) — das N×N Displacement-Array
dominiert Rechenzeit und Speicher.

---

## Nach Optimierung — Spatial Hashing + Numba JIT

| Partikel | ms/step | FPS |
|----------|---------|-----|
| 100 | 0.08 | 12500 |
| 500 | 0.13 | 7692 |
| 1000 | 0.18 | 5556 |
| 1500 | 0.25 | 4000 |
| 2000 | 0.36 | 2778 |
| 3000 | 0.62 | 1613 |

---

## Speedup-Vergleich

Gemessen mit `scripts/compare_engines.py` (beide Engines lokal, gleicher Seed).

| Partikel | Vorher (ms) | Nachher (ms) | Speedup |
|----------|-------------|--------------|---------|
| 100 | 0.25 | 0.08 | 3x |
| 500 | 5.60 | 0.13 | **45x** |
| 1000 | 22.74 | 0.18 | **127x** |
| 1500 | 50.76 | 0.25 | **201x** |
| 2000 | 90.42 | 0.36 | **250x** |
| 3000 | 185.11 | 0.62 | **297x** |

## Was wurde optimiert?

1. **Spatial Hashing** — Grid-basierte Nachbarschaftssuche, nur Partikel
   innerhalb von `MAX_RADIUS` werden berechnet (O(n) statt O(n²))
2. **Numba JIT** — Innere Schleife mit `@njit(parallel=True)` kompiliert
3. **Speicher** — Kein N×N Array mehr, nur O(n) für Partikel-Daten
