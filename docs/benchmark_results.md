# Benchmark-Ergebnisse: Performance-Optimierung (Issue #45)

**Backend:** Numba JIT + Spatial Hashing

| Partikel | ms/step | FPS | Speicher |
|----------|---------|-----|----------|
| 100 | 0.10 | 9529.8 | 0.003 MB |
| 500 | 0.27 | 3719.8 | 0.013 MB |
| 1000 | 0.43 | 2324.3 | 0.027 MB |
| 1500 | 0.73 | 1368.0 | 0.040 MB |
| 2000 | 1.13 | 883.9 | 0.053 MB |
| 3000 | 3.65 | 274.2 | 0.080 MB |
| 5000 | 6.65 | 150.4 | 0.134 MB |

## Optimierung

- **Spatial Hashing:** Grid-basierte Nachbarschaftssuche (O(n) statt O(n²))
- **Numba JIT:** Innere Berechnungsschleife mit `@njit(parallel=True)` kompiliert
- **Speicher:** Keine N×N Arrays mehr – nur O(n) Speicher für Partikel-Daten
