import numpy as np
import pytest

# Wir importieren eure Klasse aus dem Hauptordner
from particle_life.simulation import ParticleSystem


@pytest.fixture
def small_particle_system():
    """
    Create a ParticleSystem with only 10 particles and fixed random seed.
    This makes the random positions exactly the same on each test run.
    """
    # 1. Random Seed setzen: WICHTIG für reproduzierbare Tests!
    # Sonst schlagen Tests fehl, nur weil ein Partikel zufällig woanders startete.
    np.random.seed(42)
    
    # 2. System initialisieren mit kleinen, überschaubaren Werten
    # Wir überschreiben die Defaults aus der config, um isoliert zu testen.
    system = ParticleSystem(
        n_particles=10, 
        width=100, 
        height=100, 
        friction=0.5
    )
    
    return system

@pytest.fixture
def interaction_matrix_fixed():
    """
    Create a simple fixed interaction matrix for tests.
    Example: 2 types where type 0 attracts type 1.
    """
    # Beispiel: 2x2 Matrix für 2 Partikeltypen
    matrix = np.array([
        [0.0, 0.5],  # Typ 0 auf Typ 0 (neutral), Typ 0 auf Typ 1 (Anziehung)
        [-0.5, 0.0]  # Typ 1 auf Typ 0 (Abstoßung), Typ 1 auf Typ 1 (neutral)
    ])
    return matrix