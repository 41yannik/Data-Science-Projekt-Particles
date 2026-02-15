# Profiling Report

| Partikel | ms/step | FPS | Speicher |
|----------|---------|-----|----------|
| 100 | 0.24 | 4149.4 | 0.1 MB |
| 500 | 5.75 | 174.0 | 1.9 MB |
| 1000 | 23.28 | 42.9 | 7.6 MB |
| 1500 | 51.31 | 19.5 | 17.2 MB |
| 2000 | 91.79 | 10.9 | 30.5 MB |
| 3000 | 184.93 | 5.4 | 68.7 MB |

**Bottleneck:** `PhysicsEngine.step()` ist O(n²) — das N×N Displacement-Array dominiert Rechenzeit und Speicher.
