"""
Simulation module with particle system management.
"""

import numpy as np

import particle_life.config as config
from particle_life.physics import PhysicsEngine


class ParticleSystem:
    """Manages particle data, rules, and movement."""

    def __init__(
        self,
        n_particles: int | None = None,
        n_types: int | None = None,
        width: int | None = None,
        height: int | None = None,
        friction: float | None = None,
    ) -> None:
        """
        Initializes the system.

        Parameters can be overridden for tests, otherwise default values
        from config.py are used.
        """
        self.n_particles = (
            n_particles if n_particles is not None else config.PARTICLE_COUNT
        )
        self.n_types = n_types if n_types is not None else config.PARTICLE_TYPES
        self.width = width if width is not None else config.WINDOW_WIDTH
        self.height = height if height is not None else config.WINDOW_HEIGHT
        self.friction = friction if friction is not None else config.FRICTION

        self.positions = np.random.rand(self.n_particles, 2).astype(np.float32)
        self.positions[:, 0] *= self.width
        self.positions[:, 1] *= self.height

        self.velocities = np.zeros((self.n_particles, 2), dtype=np.float32)

        self.types = np.random.randint(
            0, self.n_types, size=self.n_particles, dtype=np.int32
        )

        self.interaction_matrix = np.random.uniform(
            -1, 1, (self.n_types, self.n_types)
        ).astype(np.float32)

        self.engine = PhysicsEngine(self.n_particles)

    def update(self, dt: float | None = None) -> None:
        if dt is None:
            dt = config.DT
        self.engine.step(self, float(dt))

    def get_positions(self):
        """Returns the particle positions."""
        return self.positions

    def get_types(self):
        """Returns the particle types."""
        return self.types

    def get_rules(self):
        """Returns the interaction matrix (for debugging)."""
        return self.interaction_matrix
