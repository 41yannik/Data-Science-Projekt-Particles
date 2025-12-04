"""
Core simulation module.
"""

import numpy as np


class ParticleSystem:
    """
    Diese Klasse verwaltet alle Partikel.
    Anstatt 2000 einzelne Objekte zu erstellen (was langsam ist),
    speichern wir alles in großen Tabellen (Arrays).
    """

    def __init__(self, n_particles, n_types, width, height):
        """
        Erstellt das System.

        Parameter:
        - n_particles: Anzahl der Teilchen (z.B. 1000)
        - n_types: Anzahl der Farben/Typen (z.B. 4)
        - width: Breite des Fensters
        - height: Höhe des Fensters
        """
        self.n_particles = n_particles
        self.n_types = n_types
        self.width = width
        self.height = height

        # --- 1. Positionen ---
        # Wir erstellen eine Tabelle mit Zufallszahlen zwischen 0 und 1.
        # Format: (Anzahl, 2). Das heißt: 1000 Zeilen, 2 Spalten (X und Y).
        # dtype=np.float32 spart Speicher und ist schneller auf deinem M2 Chip.
        self.positions = np.random.rand(n_particles, 2).astype(np.float32)

        # Wir strecken die Zufallszahlen (0 bis 1) auf die Bildschirmgröße
        self.positions[:, 0] *= width  # X-Koordinaten mal Breite
        self.positions[:, 1] *= height  # Y-Koordinaten mal Höhe

        # --- 2. Geschwindigkeiten ---
        # Am Anfang bewegen sich die Teilchen nicht. Wir füllen alles mit 0.
        self.velocities = np.zeros((n_particles, 2), dtype=np.float32)

        # --- 3. Farben / Typen ---
        # Jeder Partikel bekommt eine zufällige Zahl als Typ (z.B. 0, 1, 2 oder 3).
        # Das bestimmt später die Farbe (Rot, Grün, Blau, Gelb).
        self.types = np.random.randint(0, n_types, size=n_particles, dtype=np.int32)

    def get_positions(self):
        """Gibt die Tabelle mit den Positionen zurück."""
        return self.positions

    def get_types(self):
        """Gibt die Liste der Typen zurück."""
        return self.types