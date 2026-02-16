import numpy as np

import particle_life.config as config
from particle_life.simulation import ParticleSystem


def test_config_physics_boundaries_are_valid():
    assert 0.0 <= config.FRICTION <= 1.0
    assert config.DT > 0
    assert config.MIN_DISTANCE > 0
    assert config.MAX_RADIUS >= config.MIN_DISTANCE


def test_config_palette_bounds_and_type_coverage():
    assert len(config.COLOR_PALETTE) >= config.PARTICLE_TYPES
    for color in config.COLOR_PALETTE:
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)


def test_particle_system_uses_edge_like_config_values(monkeypatch):
    monkeypatch.setattr(config, "PARTICLE_COUNT", 1)
    monkeypatch.setattr(config, "PARTICLE_TYPES", 1)
    monkeypatch.setattr(config, "WINDOW_WIDTH", 1)
    monkeypatch.setattr(config, "WINDOW_HEIGHT", 1)
    monkeypatch.setattr(config, "FRICTION", 0.0)

    sim = ParticleSystem()
    sim.update(dt=0.01)

    assert sim.get_positions().shape == (1, 2)
    assert sim.get_types().shape == (1,)
    assert sim.get_rules().shape == (1, 1)
    assert np.all(sim.get_positions() >= 0)
