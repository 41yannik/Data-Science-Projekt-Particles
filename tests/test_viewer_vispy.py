import sys
import types
from types import SimpleNamespace

import numpy as np

try:
    import vispy  # noqa: F401
except ModuleNotFoundError:
    # Minimaler Stub, damit particle_life.viewer_vispy importierbar bleibt.
    sys.modules["vispy"] = types.SimpleNamespace(
        app=types.SimpleNamespace(Timer=object, run=lambda: None, quit=lambda: None),
        scene=types.SimpleNamespace(
            SceneCanvas=object,
            PanZoomCamera=object,
            visuals=types.SimpleNamespace(Markers=object, Text=object),
        ),
    )

import particle_life.viewer_vispy as vv


class _FakeKeyPressEmitter:
    def __init__(self):
        self.callbacks = []

    def connect(self, cb):
        self.callbacks.append(cb)


class _FakeEvents:
    def __init__(self):
        self.key_press = _FakeKeyPressEmitter()


class _FakePanZoomCamera:
    def __init__(self, aspect=1):
        self.aspect = aspect
        self.ranges = None

    def set_range(self, x, y):
        self.ranges = (x, y)


class _FakeView:
    def __init__(self):
        self.scene = object()
        self.camera = None


class _FakeCentralWidget:
    def __init__(self):
        self.view = _FakeView()

    def add_view(self):
        return self.view


class _FakeCanvas:
    def __init__(self, title, size, bgcolor, keys, show):
        self.title = title
        self.size = size
        self.bgcolor = bgcolor
        self.keys = keys
        self.show = show
        self.central_widget = _FakeCentralWidget()
        self.events = _FakeEvents()
        self.scene = object()
        self.closed = False

    def close(self):
        self.closed = True


class _FakeMarkers:
    def __init__(self, parent=None):
        self.parent = parent
        self.last_data = None

    def set_data(self, **kwargs):
        self.last_data = kwargs


class _FakeText:
    def __init__(self, text, color, font_size, anchor_x, anchor_y, parent):
        self.text = text
        self.color = color
        self.font_size = font_size
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.parent = parent
        self.pos = None


class _FakeTimer:
    def __init__(self, interval, connect, start):
        self.interval = interval
        self.connect = connect
        self.start = start


class _FakeApp:
    def __init__(self):
        self.run_calls = 0
        self.quit_calls = 0
        self.Timer = _FakeTimer

    def run(self):
        self.run_calls += 1

    def quit(self):
        self.quit_calls += 1


def _patch_vispy(monkeypatch):
    fake_app = _FakeApp()
    fake_scene = SimpleNamespace(
        SceneCanvas=_FakeCanvas,
        PanZoomCamera=_FakePanZoomCamera,
        visuals=SimpleNamespace(Markers=_FakeMarkers, Text=_FakeText),
    )
    monkeypatch.setattr(vv, "app", fake_app)
    monkeypatch.setattr(vv, "scene", fake_scene)
    return fake_app


class _FakeSim:
    def __init__(self):
        self.friction = 0.5
        self.n_particles = 3
        self.update_calls = 0
        self._positions = np.array(
            [[1.0, 1.0], [2.0, 3.0], [4.0, 5.0]],
            dtype=np.float32,
        )
        self._types = np.array([0, 1, 2], dtype=np.int32)

    def update(self, _dt):
        self.update_calls += 1

    def get_positions(self):
        return self._positions

    def get_types(self):
        return self._types


def test_build_color_array_maps_palette_indices(monkeypatch):
    monkeypatch.setattr(vv.config, "COLOR_PALETTE", [(10, 20, 30), (100, 110, 120)])
    out = vv._build_color_array(np.array([0, 1, 2, 3], dtype=np.int32))

    assert out.shape == (4, 4)
    assert np.allclose(out[0], [10 / 255.0, 20 / 255.0, 30 / 255.0, 1.0])
    assert np.allclose(out[2], out[0])


def test_vispy_viewer_poc_and_escape(monkeypatch):
    fake_app = _patch_vispy(monkeypatch)
    monkeypatch.setattr(vv.config, "PARTICLE_COUNT", 5)
    monkeypatch.setattr(vv.config, "PARTICLE_TYPES", 2)

    viewer = vv.VispyViewer(sim=None)

    assert viewer.is_poc is True
    assert "PoC Mode" in viewer.info_text.text

    viewer._on_key_press(SimpleNamespace(key="Escape"))
    viewer._on_key_press(SimpleNamespace(key="F"))

    assert viewer.canvas.closed is True
    assert fake_app.quit_calls == 1


def test_vispy_viewer_simulation_mode_timer_and_keys(monkeypatch):
    _patch_vispy(monkeypatch)
    monkeypatch.setattr(vv.config, "FORCE_FACTOR", 10.0)
    monkeypatch.setattr(vv.config, "MAX_RADIUS", 80.0)

    sim = _FakeSim()
    viewer = vv.VispyViewer(sim=sim)

    viewer._on_timer(None)
    assert sim.update_calls == 1
    assert viewer._step == 1

    viewer.paused = True
    viewer._on_timer(None)
    assert sim.update_calls == 1

    viewer._on_key_press(SimpleNamespace(key=" "))
    viewer._on_key_press(SimpleNamespace(key="F"))
    viewer._on_key_press(SimpleNamespace(key="G"))
    viewer._on_key_press(SimpleNamespace(key="R"))
    viewer._on_key_press(SimpleNamespace(key="E"))
    viewer._on_key_press(SimpleNamespace(key="T"))
    viewer._on_key_press(SimpleNamespace(key="Z"))

    assert viewer.paused is False
    assert 0.0 <= sim.friction <= 1.0
    assert vv.config.FORCE_FACTOR >= 0.0
    assert vv.config.MAX_RADIUS >= 0.0
    assert "step=" in viewer.info_text.text


def test_run_and_run_poc_call_app_run(monkeypatch):
    fake_app = _patch_vispy(monkeypatch)
    calls = {"sim": 0, "viewer": 0}

    class FakeSystem:
        pass

    def fake_viewer_ctor(sim=None):
        if sim is None:
            calls["viewer"] += 1
        else:
            calls["sim"] += 1
            calls["viewer"] += 1
        return SimpleNamespace()

    monkeypatch.setattr(vv, "ParticleSystem", FakeSystem)
    monkeypatch.setattr(vv, "VispyViewer", fake_viewer_ctor)
    monkeypatch.setattr(vv.config, "SEED", None)

    vv.run()
    vv.run_poc()

    assert calls["sim"] == 1
    assert calls["viewer"] == 2
    assert fake_app.run_calls == 2
