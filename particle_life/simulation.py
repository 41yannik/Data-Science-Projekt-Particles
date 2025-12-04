"""
Core simulation module.
"""

import numpy as np

# Wir importieren unsere neue Config-Datei
import particle_life.config as config


class ParticleSystem:
    """
    Verwaltet die Partikel-Daten und die Regeln (Matrix).
    """

    def __init__(self):
        """
        Initialisiert das System mit Werten aus der config.py.
        """
        self.n_particles = config.PARTICLE_COUNT
        self.n_types = config.PARTICLE_TYPES
        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT

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

    def get_positions(self):
        """Gibt die Positionen zurück."""
        return self.positions

    def get_types(self):
        """Gibt die Typen zurück."""
        return self.types

    def get_rules(self):
        """Gibt die Matrix zurück (zum Debuggen)."""
        return self.interaction_matrix