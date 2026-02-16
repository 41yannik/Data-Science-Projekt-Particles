import sys
import types

import numpy as np

import particle_life.main as main_module


def test_main_defaults_to_console(monkeypatch):
    called = {"console": 0}

    monkeypatch.setattr(
        main_module,
        "run_console",
        lambda: called.__setitem__("console", called["console"] + 1),
    )
    monkeypatch.setattr(sys, "argv", ["prog"])

    main_module.main()

    assert called["console"] == 1


def test_main_selects_viewer_mode(monkeypatch):
    called = {"viewer": 0}

    monkeypatch.setattr(
        main_module,
        "run_viewer",
        lambda: called.__setitem__("viewer", called["viewer"] + 1),
    )
    monkeypatch.setattr(sys, "argv", ["prog", "--mode", "viewer"])

    main_module.main()

    assert called["viewer"] == 1


def test_main_selects_vispy_mode(monkeypatch):
    called = {"vispy": 0}
    fake_mod = types.SimpleNamespace(
        run=lambda: called.__setitem__("vispy", called["vispy"] + 1)
    )

    monkeypatch.setitem(sys.modules, "particle_life.viewer_vispy", fake_mod)
    monkeypatch.setattr(sys, "argv", ["prog", "--mode", "vispy"])

    main_module.main()

    assert called["vispy"] == 1


def test_main_mode_flag_without_value_falls_back_to_console(monkeypatch):
    called = {"console": 0}

    monkeypatch.setattr(
        main_module,
        "run_console",
        lambda: called.__setitem__("console", called["console"] + 1),
    )
    monkeypatch.setattr(sys, "argv", ["prog", "--mode"])

    main_module.main()

    assert called["console"] == 1


def test_main_unknown_mode_falls_back_to_console(monkeypatch):
    called = {"console": 0}

    monkeypatch.setattr(
        main_module,
        "run_console",
        lambda: called.__setitem__("console", called["console"] + 1),
    )
    monkeypatch.setattr(sys, "argv", ["prog", "--mode", "unexpected"])

    main_module.main()

    assert called["console"] == 1


def test_run_console_stops_on_keyboard_interrupt(monkeypatch, capsys):
    class FakeSystem:
        def __init__(self):
            self._calls = 0

        def update(self, _dt):
            self._calls += 1
            if self._calls > 1:
                raise KeyboardInterrupt

        def get_positions(self):
            return np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)

    seed_calls = {"count": 0}
    monkeypatch.setattr(main_module.config, "SEED", 123)
    monkeypatch.setattr(
        main_module.np.random,
        "seed",
        lambda _: seed_calls.__setitem__("count", seed_calls["count"] + 1),
    )
    monkeypatch.setattr(main_module, "ParticleSystem", FakeSystem)

    main_module.run_console()

    out = capsys.readouterr().out
    assert "step=0" in out
    assert "Stopped at step 1" in out
    assert seed_calls["count"] == 1
