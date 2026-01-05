"""
Core simulation module.
"""

import numpy as np

import particle_life.config as config
from particle_life.physics import PhysicsEngine


class ParticleSystem:
    """Verwaltet die Partikel-Daten, Regeln und Bewegung."""

    def __init__(
        self,
        n_particles: int | None = None,
        n_types: int | None = None,
        width: int | None = None,
        height: int | None = None,
        friction: float | None = None,
    ) -> None:
        """
        Initialisiert das System.

        Parameter können für Tests überschrieben werden, ansonsten werden
        Standardwerte aus der config.py verwendet.
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
        """Gibt die Positionen zurück."""
        return self.positions

    def get_types(self):
        """Gibt die Typen zurück."""
        return self.types

    def get_rules(self):
        """Gibt die Matrix zurück (zum Debuggen)."""
        return self.interaction_matrix
