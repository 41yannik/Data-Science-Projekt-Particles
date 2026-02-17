"""
Unit tests for the ParticleSystem.

This test module checks the core functionality of the particle simulation,
particularly the interaction matrix and its effects on particle movement.
"""

import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem


def test_create_system():
    """
    Basic test: Check if the system is initialized correctly.

    Verifies:
    - System can be created with defined parameters
    - Positions and types arrays have correct length
    """
    # System mit definierten Parametern erstellen
    sim = ParticleSystem(n_particles=10, n_types=2, width=100, height=100)

    # Assertions: Größen prüfen
    assert len(sim.get_positions()) == 10, "Falsche Anzahl von Positionen"
    assert len(sim.get_types()) == 10, "Falsche Anzahl von Typen"


def test_friction_reduces_velocity(small_particle_system):
    """Check that friction reduces velocity."""
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
    """Check that particles wrap correctly at edges (toroidal space)."""
    sim = ParticleSystem(n_particles=1, width=100, height=100, friction=1.0)

    # Place particle exactly at right edge and move it right.
    sim.positions = np.array([[99.0, 50.0]], dtype=np.float32)
    sim.velocities = np.array([[50.0, 0.0]], dtype=np.float32)

    sim.update()

    new_x = float(sim.positions[0, 0])
    assert new_x < 5.0


def test_particles_move(small_particle_system):
    """
    Check that particle positions change after update() when velocity is set.
    """
    sim = small_particle_system

    # No interaction forces, so only velocity movement counts.
    sim.interaction_matrix[:] = 0.0
    sim.velocities = np.full((sim.n_particles, 2), [5.0, 0.0], dtype=np.float32)

    positions_before = sim.positions.copy()

    sim.update()

    positions_after = sim.positions

    assert np.any(positions_after != positions_before)


def test_interaction_rules(interaction_matrix_fixed, small_particle_system):
    """Main test: Check interaction matrix application (attraction)."""

    Dieser Test verifiziert, dass:
    1. Die Interaktionsmatrix korrekt auf Partikeltypen angewendet wird
    2. Partikel sich gemäß der Matrix bewegen (Anziehung/Abstoßung)
    3. Die Simulation das "Particle Life" Regelwerk umsetzt

    Szenario:
    --------
    - Zwei Partikel mit unterschiedlichen Typen (Typ 0, Typ 1)
    - Horizontale Anordnung mit definierten Positionen
    - Fixture-Matrix: [[0.0, 0.5], [-0.5, 0.0]]
      * matrix[0, 1] = 0.5: Typ 1 ZIEHT Typ 0 AN
      * matrix[1, 0] = -0.5: Typ 0 STÖßT Typ 1 AB
    - Beide Effekte führen dazu, dass Partikel sich AUFEINANDER ZU bewegen

    Akzeptanzkriterien:
    ------------------
    ✓ Test nutzt die Fixture interaction_matrix_fixed
    ✓ Berechnete Kraft/Bewegung entspricht der Matrix-Logik
    """
    # SETUP 
    # System mit 2 Partikeln erstellen
    sim = ParticleSystem(
        n_particles=2,
        n_types=2,
        width=200,
        height=200,
        friction=0.5
    )

    # Partikel-Positionen definieren (horizontal, 40 Einheiten Distanz)
    sim.positions = np.array([
        [50.0, 100.0],   # Partikel 0, Typ 0 (links)
        [90.0, 100.0]    # Partikel 1, Typ 1 (rechts)
    ], dtype=np.float32)

    # Partikel-Typen festlegen
    sim.types = np.array([0, 1], dtype=np.int32)

    # Geschwindigkeiten zurücksetzen (keine initiale Bewegung)
    sim.velocities = np.zeros((2, 2), dtype=np.float32)

    # Interaktionsmatrix aus Fixture einsetzen
    sim.interaction_matrix = interaction_matrix_fixed
    # Matrix: [[0.0, 0.5], [-0.5, 0.0]]

    # VORHER-MESSUNG
    pos_before = sim.positions.copy()

    # SIMULATION
    # Einen Update-Schritt ausführen
    sim.update(dt=0.01)

    # NACHHER-MESSUNG
    pos_after = sim.positions.copy()

    # Bewegungsvektoren berechnen
    movement_0 = pos_after[0] - pos_before[0]
    movement_1 = pos_after[1] - pos_before[1]

    # ASSERTIONS

    # 1. Beide Partikel müssen sich bewegt haben
    assert np.abs(movement_0[0]) > 1e-6, (
        f"Fehler: Partikel 0 hat sich nicht bewegt!\n"
        f"Bewegung: {movement_0}\n"
        f"Matrix: {interaction_matrix_fixed}"
    )

    assert np.abs(movement_1[0]) > 1e-6, (
        f"Fehler: Partikel 1 hat sich nicht bewegt!\n"
        f"Bewegung: {movement_1}\n"
        f"Matrix: {interaction_matrix_fixed}"
    )

    # 2. Beide müssen sich IN DIE GLEICHE RICHTUNG bewegen
    #    (da die asymmetrische Matrix beide aufeinander zu treibt)
    assert np.sign(movement_0[0]) == np.sign(movement_1[0]), (
        f"Fehler: Partikel bewegen sich in unterschiedliche Richtungen!\n"
        f"Das bedeutet, die Kraft ist nicht korrekt berechnet.\n"
        f"Partikel 0 Bewegung: {movement_0}\n"
        f"Partikel 1 Bewegung: {movement_1}\n"
        f"Matrix: {interaction_matrix_fixed}"
    )

    # 3. Gesamtbewegung muss signifikant sein (nicht nur Rauschen)
    total_movement = np.linalg.norm(movement_0) + np.linalg.norm(movement_1)
    assert total_movement > 1e-5, (
        f"Fehler: Zu wenig Gesamtbewegung!\n"
        f"Total: {total_movement}\n"
        f"Partikel 0: {movement_0}\n"
        f"Partikel 1: {movement_1}"
    )


def test_interaction_rules_repulsion():
    """
    Bonus test: Check interaction matrix application (repulsion).

    This test checks the opposite scenario:
    When both particles experience REPULSIVE forces.

    Scenario:
    --------
    - Two particles side by side
    - Repulsive matrix: [[0.0, -0.5], [-0.5, 0.0]]
      * Both particles repel each other
    - Expected: Particles move AWAY FROM each other

    Acceptance criteria:
    -------------------
    * Particles move in different directions
    * Force direction is calculated correctly
    """
    # SETUP
    sim = ParticleSystem(
        n_particles=2,
        n_types=2,
        width=200,
        height=200,
        friction=0.5
    )

    # Positionen (gleiche wie bei Anziehungs-Test)
    sim.positions = np.array([
        [50.0, 100.0],   # Partikel 0 (links)
        [90.0, 100.0]    # Partikel 1 (rechts)
    ], dtype=np.float32)

    sim.types = np.array([0, 1], dtype=np.int32)
    sim.velocities = np.zeros((2, 2), dtype=np.float32)

    # REPULSIVE Matrix setzen
    repulsive_matrix = np.array([
        [0.0, -0.5],   # Typ 1 stößt Typ 0 ab
        [-0.5, 0.0]    # Typ 0 stößt Typ 1 ab
    ], dtype=np.float32)
    sim.interaction_matrix = repulsive_matrix

    # VORHER-MESSUNG
    pos_before = sim.positions.copy()

    # SIMULATION
    sim.update(dt=0.01)

    # NACHHER-MESSUNG
    pos_after = sim.positions.copy()

    movement_0 = pos_after[0] - pos_before[0]
    movement_1 = pos_after[1] - pos_before[1]

    # ASSERTIONS

    # 1. Partikel müssen sich IN UNTERSCHIEDLICHE Richtungen bewegen
    #    (voneinander weg)
    assert np.sign(movement_0[0]) != np.sign(movement_1[0]), (
        f"Fehler: Abstoßung nicht erkannt!\n"
        f"Partikel sollten sich VONEINANDER WEG bewegen.\n"
        f"Partikel 0 Bewegung: {movement_0}\n"
        f"Partikel 1 Bewegung: {movement_1}\n"
        f"Matrix: {repulsive_matrix}"
    )

    # 2. Beide müssen sich signifikant bewegt haben
    assert np.abs(movement_0[0]) > 1e-6, (
        f"Fehler: Partikel 0 hat sich nicht genug bewegt!\n"
        f"Bewegung: {movement_0}"
    )

    assert np.abs(movement_1[0]) > 1e-6, (
        f"Fehler: Partikel 1 hat sich nicht genug bewegt!\n"
        f"Bewegung: {movement_1}"
    )
