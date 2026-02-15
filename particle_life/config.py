"""
Konfiguration für die Simulation (Particle Life).
Zentrale Verwaltung aller Parameter für Physik, Fenster und Logik.
"""

# --- Allgemeine Einstellungen ---
# Setze einen Seed für reproduzierbare Ergebnisse (z.B. 42).
# Setze auf None, um bei jedem Start eine zufällige Simulation zu erhalten.
SEED = 42

# --- Fenstereinstellungen ---
WINDOW_WIDTH = 800  #: The width of the simulation window in pixels.
WINDOW_HEIGHT = 800 #: The height of the simulation window in pixels.
TITLE = "Particle Life - Student Project" #: The title shown in the window header.
BACKGROUND_COLOR = (20, 20, 20) #: Dark gray background color (RGB).

# --- Partikel Einstellungen ---
PARTICLE_COUNT = 1000 #: Total number of particles in the simulation.
PARTICLE_TYPES = 4   #: Number of distinct color-coded particle types.

# Farbpalette für die Typen (RGB Format)
# Wir definieren sie hier fest, damit die Visualisierung konsistent bleibt.
# Format: (R, G, B)
COLOR_PALETTE = [
    (255, 0, 0),    # Rot
    (0, 255, 0),    # Grün
    (0, 0, 255),    # Blau
    (255, 255, 0),  # Gelb
    (0, 255, 255),  # Cyan (Reserve)
    (255, 0, 255),  # Magenta (Reserve)
]

# --- Physik Parameter ---
DT = 0.1 #: Simulation time step (delta time).

# Friction factor (0.0 to 1.0).
# Multiplied with velocity each step (0.95 = 5% speed loss).
FRICTION = 0.95

# Maximum strength of force (attraction/repulsion) between particles.
FORCE_FACTOR = 10.0

# Maximum distance for particle interaction (unit radius).
MAX_RADIUS = 80.0

# Minimum distance to prevent division by zero during force calculations.
MIN_DISTANCE = 5.0