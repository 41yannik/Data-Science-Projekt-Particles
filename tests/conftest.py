import numpy as np
import pytest

# Wir importieren eure Klasse aus dem Hauptordner
from particle_life.simulation import ParticleSystem

@pytest.fixture
def small_particle_system():
    """
    Erstellt ein ParticleSystem mit nur 10 Partikeln und festem Random-Seed.
    Dadurch sind die 'zufälligen' Positionen bei jedem Testlauf exakt gleich.
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
    Erzeugt eine einfache, feste Interaktionsmatrix für Tests.
    Z.B. 2 Typen: Typ 0 zieht Typ 1 an.
    """
    # Beispiel: 2x2 Matrix für 2 Partikeltypen
    matrix = np.array([
        [0.0, 0.5],  # Typ 0 auf Typ 0 (neutral), Typ 0 auf Typ 1 (Anziehung)
        [-0.5, 0.0]  # Typ 1 auf Typ 0 (Abstoßung), Typ 1 auf Typ 1 (neutral)
    ])
    return matrix