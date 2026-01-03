import numpy as np

import particle_life.config as config


class PhysicsEngine:
    def __init__(self, n_particles: int) -> None:
        self._disp = np.empty((n_particles, n_particles, 2), dtype=np.float32)
        self._dist2 = np.empty((n_particles, n_particles), dtype=np.float32)
        self._within = np.empty((n_particles, n_particles), dtype=bool)
        self._force_dir = np.empty((n_particles, n_particles, 2), dtype=np.float32)
        self._force_mag = np.empty((n_particles, n_particles), dtype=np.float32)
        self._total_force = np.empty((n_particles, 2), dtype=np.float32)

    def step(self, system, dt: float) -> None:
        dt32 = np.float32(dt)
        friction = np.float32(system.friction)
        r_max = np.float32(config.MAX_RADIUS)
        force_factor = np.float32(config.FORCE_FACTOR)
        min_distance = np.float32(config.MIN_DISTANCE)

        disp = self._disp
        dist2 = self._dist2
        within = self._within
        force_dir = self._force_dir
        force_mag = self._force_mag
        total_force = self._total_force

        positions = system.positions
        velocities = system.velocities
        types = system.types

        np.subtract(positions[:, None, :], positions[None, :, :], out=disp)
        np.sum(disp * disp, axis=2, out=dist2)

        np.fill_diagonal(dist2, np.inf)

        np.less(dist2, r_max * r_max, out=within)
        if not within.any():
            positions += velocities * dt32
            velocities *= friction
            self._apply_wrap_boundaries(positions, system.width, system.height)
            return

        dist = np.sqrt(dist2, dtype=np.float32)
        dist[within] = np.maximum(dist[within], min_distance)
        np.copyto(force_mag, 1.0 - dist / r_max, where=within)
        force_mag[~within] = 0.0

        inv_dist = np.divide(1.0, dist, out=dist, where=within)
        inv_dist[~within] = 0.0
        force_dir[:] = disp * inv_dist[..., None]

        pair_strength = system.interaction_matrix[
            types[:, None],
            types[None, :],
        ]
        np.multiply(pair_strength, force_mag, out=force_mag)
        force_mag *= force_factor

        np.sum(force_mag[..., None] * force_dir, axis=1, out=total_force)

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
        positions[:, 0] = np.mod(positions[:, 0], width)
        positions[:, 1] = np.mod(positions[:, 1], height)
