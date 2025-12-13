"""
Core simulation module.
"""

import numpy as np

# Wir importieren unsere neue Config-Datei
import particle_life.config as config


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

        # --- 1. Positionen & Geschwindigkeiten ---
        # Zufällige Positionen auf dem Bildschirm
        self.positions = np.random.rand(self.n_particles, 2).astype(np.float32)
        self.positions[:, 0] *= self.width
        self.positions[:, 1] *= self.height

        # Startgeschwindigkeit ist 0
        self.velocities = np.zeros((self.n_particles, 2), dtype=np.float32)

        # --- 2. Typen (Farben) ---
        # Zufällige Zuordnung der Typen (0 bis n_types-1)
        self.types = np.random.randint(
            0, self.n_types, size=self.n_particles, dtype=np.int32
        )

        # --- 3. Die Interaktions-Matrix (Das Regelwerk) ---
        # Eine Tabelle (Größe: Typen x Typen) mit Werten zwischen -1 und 1.
        # Beispiel: matrix[0][1] = 0.5 bedeutet: Typ 0 wird von Typ 1 angezogen.
        self.interaction_matrix = np.random.uniform(
            -1, 1, (self.n_types, self.n_types)
        ).astype(np.float32)

        # Vorallocierte Puffer für O(N²)-Berechnungen (Performance)
        self._disp = np.empty((self.n_particles, self.n_particles, 2), dtype=np.float32)
        self._dist2 = np.empty((self.n_particles, self.n_particles), dtype=np.float32)
        self._within = np.empty((self.n_particles, self.n_particles), dtype=bool)
        self._force_dir = np.empty_like(self._disp)
        self._force_mag = np.empty_like(self._dist2)
        self._total_force = np.empty((self.n_particles, 2), dtype=np.float32)

    def update(self, dt: float | None = None) -> None:
        """
        Aktualisiert Positionen und Geschwindigkeiten für einen Zeitschritt.

        Args:
            dt: Zeitschritt. Wenn None wird config.DT verwendet.
        """
        if dt is None:
            dt = config.DT

        dt = np.float32(dt)
        friction = np.float32(self.friction)
        r_max = np.float32(config.MAX_RADIUS)
        force_factor = np.float32(config.FORCE_FACTOR)
        min_distance = np.float32(config.MIN_DISTANCE)

        disp = self._disp
        dist2 = self._dist2
        within = self._within
        force_dir = self._force_dir
        force_mag = self._force_mag
        total_force = self._total_force

        # Paarweise Differenzen (N x N x 2)
        np.subtract(self.positions[:, None, :], self.positions[None, :, :], out=disp)
        np.sum(disp * disp, axis=2, out=dist2)

        # Selbstwechselwirkung ausschließen
        np.fill_diagonal(dist2, np.inf)

        # Nur Nachbarn im Radius r_max
        np.less(dist2, r_max * r_max, out=within)
        if not within.any():
            self.positions += self.velocities * dt
            self.velocities *= friction
            self._apply_wrap_boundaries()
            return

        # Distanzen + Falloff
        dist = np.sqrt(dist2, dtype=np.float32)  # kleines temporäres Array
        # Mindestabstand, um Division durch 0 zu vermeiden
        dist[within] = np.maximum(dist[within], min_distance)
        np.copyto(force_mag, 1.0 - dist / r_max, where=within)
        force_mag[~within] = 0.0  # außerhalb des Radius keine Kraft

        # Richtungsvektoren normalisieren; wo not within -> 0
        inv_dist = np.divide(1.0, dist, out=dist, where=within)  # dist wird zu inv_dist
        inv_dist[~within] = 0.0
        force_dir[:] = disp * inv_dist[..., None]

        # Stärke aus Interaktionsmatrix pro Typenpaar
        pair_strength = self.interaction_matrix[
            self.types[:, None],
            self.types[None, :]
        ]
        np.multiply(pair_strength, force_mag, out=force_mag)
        force_mag *= force_factor

        # Gesamtbeschleunigung (Summe aller Beiträge)
        np.sum(force_mag[..., None] * force_dir, axis=1, out=total_force)

        # Geschwindigkeit und Position updaten
        self.velocities += total_force * dt
        self.positions += self.velocities * dt

        # Reibung & Randbedingungen
        self.velocities *= friction
        self._apply_wrap_boundaries()

    def _apply_wrap_boundaries(self) -> None:
        """Wendet Torus-Logik auf alle Partikel an."""

        self.positions[:, 0] = np.mod(self.positions[:, 0], self.width)
        self.positions[:, 1] = np.mod(self.positions[:, 1], self.height)

    def get_positions(self):
        """Gibt die Positionen zurück."""
        return self.positions

    def get_types(self):
        """Gibt die Typen zurück."""
        return self.types

    def get_rules(self):
        """Gibt die Matrix zurück (zum Debuggen)."""
        return self.interaction_matrix
