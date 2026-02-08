import numpy as np

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
