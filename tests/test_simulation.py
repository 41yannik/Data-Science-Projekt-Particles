import sys
import os

# --- Der Hack: Wir zeigen Python den Weg zum Hauptordner ---
# Wir sagen: "Nimm den Pfad dieser Datei, geh einen Schritt zurück (..),
# und such dort nach Modulen."
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..')
sys.path.insert(0, os.path.abspath(parent_dir))
# -----------------------------------------------------------

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