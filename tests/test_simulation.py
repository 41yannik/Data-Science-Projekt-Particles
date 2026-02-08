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
