"""
Configuration for particle life simulation.
Manages all parameters for physics, window, and particle settings.
"""

# General settings
# Set a seed for reproducible results (e.g., 42).
# Set to None to get a random simulation on each start.
SEED = 42

# Window settings
WINDOW_WIDTH = 800  # The width of the simulation window in pixels.
WINDOW_HEIGHT = 800  # The height of the simulation window in pixels.
TITLE = "Particle Life - Student Project"  # The title shown in the window header.
BACKGROUND_COLOR = (20, 20, 20)  # Dark gray background color (RGB).

# Particle settings
PARTICLE_COUNT = 2000  # Total number of particles in the simulation.
PARTICLE_TYPES = 4  # Number of distinct color-coded particle types.

# Color palette for particle types (RGB format)
# We define them here to keep visualization consistent.
# Format: (R, G, B)
COLOR_PALETTE = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan (spare)
    (255, 0, 255),  # Magenta (spare)
]

# Physics parameters
DT = 0.1  # Simulation time step (delta time).

# Friction factor. Multiplied with velocity each step (0.95 = 5% speed loss).
FRICTION = 0.95

# Maximum strength of force (attraction/repulsion) between particles.
FORCE_FACTOR = 10.0

# Maximum distance for particle interaction (unit radius).
MAX_RADIUS = 80.0

# Minimum distance to prevent division by zero during force calculations.
MIN_DISTANCE = 5.0