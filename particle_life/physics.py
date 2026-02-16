"""
Optimierte Physik-Engine mit Spatial Hashing und Numba JIT (Issue #45).

Ersetzt die O(n²) Brute-Force-Berechnung durch eine Grid-basierte
Nachbarschaftssuche (Spatial Hashing), sodass nur Partikelpaare innerhalb
von MAX_RADIUS berechnet werden.  Durchschnittliche Komplexität: O(n).

Falls Numba installiert ist, wird die innere Berechnungsschleife per
@njit kompiliert. Ansonsten wird ein reiner NumPy-Fallback verwendet.
"""

import numpy as np

import particle_life.config as config

# ---------------------------------------------------------------------------
# Versuche Numba zu importieren; setze Flag für Fallback
# ---------------------------------------------------------------------------
try:
    import numba  # noqa: F401
    from numba import njit, prange

    HAS_NUMBA = True
except ImportError:  # pragma: no cover
    HAS_NUMBA = False


# ===================================================================
# Numba-kompilierte Kernfunktionen
# ===================================================================
if HAS_NUMBA:

    @njit(cache=True)
    def _build_cell_lists(
        positions: np.ndarray,
        cell_size: float,
        grid_w: int,
        grid_h: int,
    ):
        """Ordnet jede Partikel der passenden Gitterzelle zu.

        Returns
        -------
        cell_counts : ndarray (grid_h, grid_w) – Anzahl Partikel pro Zelle
        cell_indices : ndarray (grid_h, grid_w, max_per_cell) – Partikel-IDs
        """
        n = positions.shape[0]
        max_per_cell = n  # Worst case: alle in einer Zelle
        cell_counts = np.zeros((grid_h, grid_w), dtype=np.int32)
        cell_indices = np.empty((grid_h, grid_w, max_per_cell), dtype=np.int32)

        for i in range(n):
            cx = int(positions[i, 0] / cell_size) % grid_w
            cy = int(positions[i, 1] / cell_size) % grid_h
            idx = cell_counts[cy, cx]
            cell_indices[cy, cx, idx] = i
            cell_counts[cy, cx] = idx + 1

        return cell_counts, cell_indices

    @njit(parallel=True, cache=True)
    def _compute_forces_numba(
        positions: np.ndarray,
        types: np.ndarray,
        interaction_matrix: np.ndarray,
        cell_counts: np.ndarray,
        cell_indices: np.ndarray,
        cell_size: float,
        grid_w: int,
        grid_h: int,
        r_max: float,
        force_factor: float,
        min_distance: float,
        width: float,
        height: float,
        total_force: np.ndarray,
    ):
        """Berechnet Kräfte mit Spatial Hashing – nur Nachbarzellen."""
        n = positions.shape[0]
        r_max_sq = r_max * r_max
        half_w = width * 0.5
        half_h = height * 0.5

        # Parallelisiert über alle Partikel
        for i in prange(n):
            fx = np.float32(0.0)
            fy = np.float32(0.0)

            cx_i = int(positions[i, 0] / cell_size) % grid_w
            cy_i = int(positions[i, 1] / cell_size) % grid_h

            # Iteriere über 3×3 Nachbarschaft
            for dcx in range(-1, 2):
                for dcy in range(-1, 2):
                    nx_c = (cx_i + dcx) % grid_w
                    ny_c = (cy_i + dcy) % grid_h
                    count = cell_counts[ny_c, nx_c]

                    for k in range(count):
                        j = cell_indices[ny_c, nx_c, k]
                        if j == i:
                            continue

                        # Displacement mit toroidalem Wrapping
                        dx = positions[j, 0] - positions[i, 0]
                        dy = positions[j, 1] - positions[i, 1]

                        # Shortest toroidal distance
                        if dx > half_w:
                            dx -= width
                        elif dx < -half_w:
                            dx += width
                        if dy > half_h:
                            dy -= height
                        elif dy < -half_h:
                            dy += height

                        dist_sq = dx * dx + dy * dy
                        if dist_sq >= r_max_sq or dist_sq == 0.0:
                            continue

                        dist = np.sqrt(dist_sq)
                        if dist < min_distance:
                            dist = min_distance

                        # Normierte Kraft (1 bei dist=0, 0 bei dist=r_max)
                        mag = np.float32(1.0) - dist / r_max

                        # Interaktionsmatrix nachschlagen
                        strength = interaction_matrix[types[i], types[j]]
                        mag *= strength * force_factor

                        # Richtungsvektor (normiert)
                        inv_dist = np.float32(1.0) / dist
                        fx += mag * dx * inv_dist
                        fy += mag * dy * inv_dist

            total_force[i, 0] = fx
            total_force[i, 1] = fy


# ===================================================================
# NumPy-Fallback (ohne Numba)
# ===================================================================
def _build_cell_lists_numpy(
    positions: np.ndarray,
    cell_size: float,
    grid_w: int,
    grid_h: int,
):
    """Erstellt Zell-Listen mit reinem NumPy."""
    cx = (positions[:, 0] / cell_size).astype(np.int32) % grid_w
    cy = (positions[:, 1] / cell_size).astype(np.int32) % grid_h
    cell_id = cy * grid_w + cx

    # Sortiere Partikel nach Zell-ID
    order = np.argsort(cell_id)
    sorted_cell_id = cell_id[order]

    # Finde Start/Ende jeder Zelle
    total_cells = grid_w * grid_h
    starts = np.zeros(total_cells, dtype=np.int32)
    counts = np.zeros(total_cells, dtype=np.int32)

    unique, unique_counts = np.unique(sorted_cell_id, return_counts=True)
    cumsum = np.cumsum(unique_counts)
    starts[unique] = cumsum - unique_counts
    counts[unique] = unique_counts

    return order, starts, counts, cell_id


def _compute_forces_numpy(
    positions: np.ndarray,
    types: np.ndarray,
    interaction_matrix: np.ndarray,
    order: np.ndarray,
    starts: np.ndarray,
    counts: np.ndarray,
    cell_size: float,
    grid_w: int,
    grid_h: int,
    r_max: float,
    force_factor: float,
    min_distance: float,
    width: float,
    height: float,
    total_force: np.ndarray,
):
    """Berechnet Kräfte mit Spatial Hashing – reiner NumPy-Fallback."""
    n = positions.shape[0]
    r_max_sq = r_max * r_max
    half_w = width * 0.5
    half_h = height * 0.5

    total_force[:] = 0.0

    for i in range(n):
        cx_i = int(positions[i, 0] / cell_size) % grid_w
        cy_i = int(positions[i, 1] / cell_size) % grid_h

        # 3×3 Nachbarschaft
        for dcx in range(-1, 2):
            for dcy in range(-1, 2):
                nx_c = (cx_i + dcx) % grid_w
                ny_c = (cy_i + dcy) % grid_h
                cid = ny_c * grid_w + nx_c
                c_start = starts[cid]
                c_count = counts[cid]
                if c_count == 0:
                    continue

                # Alle Partikel in dieser Zelle
                js = order[c_start : c_start + c_count]
                js = js[js != i]
                if len(js) == 0:
                    continue

                dx = positions[js, 0] - positions[i, 0]
                dy = positions[js, 1] - positions[i, 1]

                # Toroidales Wrapping
                dx = np.where(dx > half_w, dx - width, dx)
                dx = np.where(dx < -half_w, dx + width, dx)
                dy = np.where(dy > half_h, dy - height, dy)
                dy = np.where(dy < -half_h, dy + height, dy)

                dist_sq = dx * dx + dy * dy
                mask = (dist_sq < r_max_sq) & (dist_sq > 0.0)
                if not mask.any():
                    continue

                dx = dx[mask]
                dy = dy[mask]
                dist_sq = dist_sq[mask]
                js_m = js[mask]

                dist = np.sqrt(dist_sq).astype(np.float32)
                dist = np.maximum(dist, min_distance)

                mag = (1.0 - dist / r_max).astype(np.float32)
                strength = interaction_matrix[types[i], types[js_m]]
                mag *= strength * force_factor

                inv_dist = 1.0 / dist
                total_force[i, 0] += np.sum(mag * dx * inv_dist)
                total_force[i, 1] += np.sum(mag * dy * inv_dist)


# ===================================================================
# Öffentliche PhysicsEngine-Klasse
# ===================================================================
class PhysicsEngine:
    """Performante Physik-Engine mit Spatial Hashing.

    Nutzt Numba JIT wenn verfügbar, fällt sonst auf NumPy zurück.
    """

    def __init__(self, n_particles: int) -> None:
        self._total_force = np.empty((n_particles, 2), dtype=np.float32)
        self._numba_warmed_up = False

    def step(self, system, dt: float) -> None:
        """Berechnet und wendet den nächsten Simulationsschritt an.

        Uses Spatial Hashing to achieve O(n) average complexity instead
        of O(n²) brute force.

        Args:
            system: The ParticleSystem instance containing particle data.
            dt (float): Time step (delta time) for the integration.
        """
        dt32 = np.float32(dt)
        friction = np.float32(system.friction)
        r_max = np.float32(config.MAX_RADIUS)
        force_factor = np.float32(config.FORCE_FACTOR)
        min_distance = np.float32(config.MIN_DISTANCE)
        width = np.float32(system.width)
        height = np.float32(system.height)

        positions = system.positions
        velocities = system.velocities
        types = system.types
        interaction_matrix = system.interaction_matrix.astype(np.float32)

        total_force = self._total_force

        # Grid-Dimensionen
        cell_size = float(r_max)
        grid_w = max(1, int(np.ceil(width / cell_size)))
        grid_h = max(1, int(np.ceil(height / cell_size)))

        if HAS_NUMBA:
            # --- Numba-Pfad ---
            cell_counts, cell_indices = _build_cell_lists(
                positions, cell_size, grid_w, grid_h,
            )
            _compute_forces_numba(
                positions, types, interaction_matrix,
                cell_counts, cell_indices,
                cell_size, grid_w, grid_h,
                r_max, force_factor, min_distance,
                width, height, total_force,
            )
        else:
            # --- NumPy-Fallback ---
            order, starts, counts, _ = _build_cell_lists_numpy(
                positions, cell_size, grid_w, grid_h,
            )
            _compute_forces_numpy(
                positions, types, interaction_matrix,
                order, starts, counts,
                cell_size, grid_w, grid_h,
                r_max, force_factor, min_distance,
                width, height, total_force,
            )

        velocities += total_force * dt32
        positions += velocities * dt32
        velocities *= friction
        self._apply_wrap_boundaries(positions, system.width, system.height)

    def _apply_wrap_boundaries(
        self,
        positions: np.ndarray,
        width: int,
        height: int,
    ) -> None:
        """Applies toroidal (wrap-around) boundaries to particle positions.

        Args:
            positions (np.ndarray): Array of particle positions (Nx2).
            width (int): Width of the simulation area.
            height (int): Height of the simulation area.
        """
        positions[:, 0] = np.mod(positions[:, 0], width)
        positions[:, 1] = np.mod(positions[:, 1], height)
