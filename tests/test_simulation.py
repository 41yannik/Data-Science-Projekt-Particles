import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem


def test_create_system():
    """
    Ein einfacher Test, der prüft, ob wir das System erstellen können.
    """
    # Wir erstellen ein System mit kleinen Werten
    sim = ParticleSystem(n_particles=10, n_types=2, width=100, height=100)

    # Wir prüfen, ob die Arrays die richtige Größe haben
    assert len(sim.get_positions()) == 10
    assert len(sim.get_types()) == 10


def test_friction_reduces_velocity(small_particle_system):
    """
    Prüft, dass die Reibung die Geschwindigkeit reduziert.
    """
    system = small_particle_system

    # Partikel weit auseinander, aber innerhalb des Fensters platzieren.
    spacing = min(config.MAX_RADIUS * 2.5, system.width / system.n_particles * 0.9)
    x_positions = np.arange(system.n_particles, dtype=np.float32) * spacing
    x_positions = np.mod(x_positions, system.width)
    positions = np.zeros((system.n_particles, 2), dtype=np.float32)
    positions[:, 0] = x_positions
    positions[:, 1] = system.height * 0.5
    system.positions = positions

    # Interaktionsmatrix auf 0 setzen, um Kräfte auszuschließen.
    system.interaction_matrix[:] = 0.0

    # Hohe Startgeschwindigkeit vergeben.
    system.velocities = np.full((system.n_particles, 2), 10.0, dtype=np.float32)

    speed_before = np.linalg.norm(system.velocities, axis=1)

    system.update()

    speed_after = np.linalg.norm(system.velocities, axis=1)

    assert np.all(speed_after < speed_before)
