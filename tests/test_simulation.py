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


def test_boundary_wrapping():
    """
    Prüft, dass Partikel am Rand korrekt gewrappt werden (Torus).
    """
    sim = ParticleSystem(n_particles=1, width=100, height=100, friction=1.0)

    # Partikel exakt an den rechten Rand setzen und nach rechts bewegen.
    sim.positions = np.array([[99.0, 50.0]], dtype=np.float32)
    sim.velocities = np.array([[50.0, 0.0]], dtype=np.float32)

    sim.update()

    new_x = float(sim.positions[0, 0])
    assert new_x < 5.0



def test_particles_move(small_particle_system):
    """
    Prüft, dass sich Partikelpositionen nach update() verändern,
    wenn eine Geschwindigkeit gesetzt ist.
    """
    sim = small_particle_system

    # Keine Interaktionskräfte, damit nur Bewegung durch Velocity zählt.
    sim.interaction_matrix[:] = 0.0
    sim.velocities = np.full((sim.n_particles, 2), [5.0, 0.0], dtype=np.float32)

    positions_before = sim.positions.copy()

    sim.update()

    positions_after = sim.positions

    assert np.any(positions_after != positions_before)

