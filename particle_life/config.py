"""
Konfiguration für die Simulation (Particle Life).
Zentrale Verwaltung aller Parameter für Physik, Fenster und Logik.
"""

# --- Allgemeine Einstellungen ---
# Setze einen Seed für reproduzierbare Ergebnisse (z.B. 42).
# Setze auf None, um bei jedem Start eine zufällige Simulation zu erhalten.
SEED = 42

# --- Fenstereinstellungen ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
TITLE = "Particle Life - Student Project"
BACKGROUND_COLOR = (20, 20, 20) # Dunkles Grau für bessere Sichtbarkeit

# --- Partikel Einstellungen ---
# Anzahl der Partikel (1000 ist gut für M2 Chips)
PARTICLE_COUNT = 1000

# Anzahl der Farben/Typen
PARTICLE_TYPES = 4

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
# Zeitschritt: Delta Time pro Berechnungsschritt
DT = 0.1

# Reibung (Friction): 0.0 bis 1.0
# Faktor, mit dem die Geschwindigkeit pro Schritt multipliziert wird.
# 0.95 = 5% Geschwindigkeitsverlust pro Tick (Dämpfung).
FRICTION = 0.95

# Kraftfaktor: Wie stark stoßen/ziehen sich Teilchen maximal an?
FORCE_FACTOR = 10.0

# Wirkungsradius: Wie weit können Partikel "sehen"?
# Nur Partikel innerhalb dieses Radius üben Kräfte aufeinander aus.
MAX_RADIUS = 80.0

# Minimaler Abstand, um Division durch Null bei der Kraftberechnung zu vermeiden
MIN_DISTANCE = 5.0