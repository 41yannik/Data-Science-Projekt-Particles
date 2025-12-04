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