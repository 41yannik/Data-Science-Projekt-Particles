import pytest
import numpy as np

# ANPASSUNG: Der Code liegt im Ordner 'particle_life'
# Wir importieren also aus dem Package.
from particle_life.simulation import ParticleSimulation
import particle_life.config as config

# --- FIXTURE ---
@pytest.fixture
def sim_config():
    """
    Erstellt eine Standard-Simulation für Tests.
    Nutzt einen festen Seed für Reproduzierbarkeit.
    """
    np.random.seed(42)
    # Erstelle Simulation (Parameter anpassen falls nötig)
    sim = ParticleSimulation(n_particles=10, area_size=100.0)
    return sim

# --- TESTS ---

def test_initialization_state(sim_config):
    """Smoke Test: Startet die Simulation überhaupt?"""
    assert len(sim_config.positions) == 10
    assert sim_config.positions.shape == (10, 2)

def test_no_nans_after_update(sim_config):
    """
    Issue #22: Prüft, ob die Simulation stabil läuft (keine NaNs).
    """
    for _ in range(10):
        sim_config.step()
    
    # Prüfen, ob irgendein Wert ungültig (NaN) ist
    assert not np.isnan(sim_config.positions).any(), "Fehler: Positionen enthalten NaNs"
    assert not np.isnan(sim_config.velocities).any(), "Fehler: Geschwindigkeiten enthalten NaNs"

def test_boundary_wrap():
    """
    Issue #22: Prüft, ob Partikel am Rand auf die andere Seite springen.
    """
    sim = ParticleSimulation(n_particles=1, area_size=100.0)
    
    # Partikel kurz vor den rechten Rand setzen
    sim.positions[0] = [99.0, 50.0]
    sim.velocities[0] = [2.0, 0.0] 
    
    sim.step()
    
    new_x = sim.positions[0][0]
    
    # Erwartung: Partikel ist gewrapped (z.B. bei 1.0), nicht bei 101.0
    assert 0.0 <= new_x < 100.0, f"Partikel ist außerhalb des Feldes: {new_x}"
    assert new_x < 10.0, "Wrapping hat nicht funktioniert"

def test_force_cutoff_radius(monkeypatch):
    """
    Issue #22: Prüft, ob weit entfernte Partikel sich ignorieren.
    """
    # Wir setzen den MAX_RADIUS in der config temporär auf 1.0
    monkeypatch.setattr(config, "MAX_RADIUS", 1.0)
    
    sim = ParticleSimulation(n_particles=2, area_size=100.0)
    
    # Partikel weit auseinander platzieren
    sim.positions[0] = [0.0, 0.0]
    sim.positions[1] = [50.0, 0.0]
    sim.velocities[:] = 0.0
    
    sim.step()
    
    # Keine Kraft = Keine Bewegung (bei Startgeschwindigkeit 0)
    assert np.allclose(sim.velocities, 0.0), "Geschwindigkeit trotz großer Distanz geändert"

def test_minimum_distance_repulsion(monkeypatch):
    """
    Issue #22: Prüft, ob sich nahe Partikel abstoßen.
    """
    # Erzwinge eine Mindestdistanz für den Test
    monkeypatch.setattr(config, "MIN_DISTANCE", 2.0)

    sim = ParticleSimulation(n_particles=2, area_size=100.0)
    
    # Extrem nah beieinander
    sim.positions[0] = [50.0, 50.0]
    sim.positions[1] = [50.1, 50.0]
    sim.velocities[:] = 0.0
    
    dist_before = np.linalg.norm(sim.positions[0] - sim.positions[1])
    
    sim.step()
    
    dist_after = np.linalg.norm(sim.positions[0] - sim.positions[1])
    
    assert dist_after > dist_before, "Abstoßung hat nicht funktioniert"