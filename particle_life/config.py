"""
Konfiguration für die Simulation.
Hier stellen wir alle Parameter ein.
"""

# --- Fenstereinstellungen ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
TITLE = "Particle Life - Student Project"

# --- Simulationseinstellungen ---
# Anzahl der Partikel (1000 ist gut für den Anfang)
PARTICLE_COUNT = 1000

# Anzahl der Farben/Typen (z.B. 4: Rot, Grün, Blau, Gelb)
PARTICLE_TYPES = 4

# --- Physik Parameter ---
# Zeitschritt: Wie schnell vergeht die Zeit pro Berechnung?
DT = 0.1

# Reibung (0.0 bis 1.0).
# Wichtig, damit Teilchen nicht unendlich schnell werden.
# 0.95 bedeutet: Pro Schritt behalten sie 95% ihrer Geschwindigkeit.
FRICTION = 0.95

# Maximale Kraft, die ausgeübt werden kann
FORCE_FACTOR = 10.0

# Wie weit können Partikel sehen?
MAX_RADIUS = 80.0