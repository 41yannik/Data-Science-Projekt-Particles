import numpy as np
import pytest

import particle_life.viewer as viewer


@pytest.fixture
def dummy_pygame_env(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")


def test_button_draw_and_click(dummy_pygame_env):
    viewer.pygame.init()
    try:
        font = viewer.pygame.font.SysFont(None, 18)
        surface = viewer.pygame.Surface((120, 60))
        clicked = {"count": 0}
        button = viewer.Button(
            rect=viewer.pygame.Rect(10, 10, 80, 30),
            text="A",
            font=font,
            callback=lambda: clicked.__setitem__("count", clicked["count"] + 1),
            base_color=(10, 10, 10),
            hover_color=(20, 20, 20),
            text_color=(255, 255, 255),
            dynamic_text=lambda: "D",
        )

        button.handle_event(
            viewer.pygame.event.Event(
                viewer.pygame.MOUSEMOTION,
                {"pos": (15, 15)},
            )
        )
        button.draw(surface)
        button.handle_event(
            viewer.pygame.event.Event(
                viewer.pygame.MOUSEBUTTONDOWN,
                {"button": 1, "pos": (15, 15)},
            )
        )

        assert button.hovered is True
        assert clicked["count"] == 1
    finally:
        viewer.pygame.quit()


def test_run_smoke_exits_cleanly(monkeypatch, dummy_pygame_env):
    class FakeClock:
        def get_fps(self):
            return 60.0

        def tick(self, _fps):
            return None

    class FakeSystem:
        def __init__(self):
            self.friction = 0.5
            self.update_calls = 0
            self._positions = np.array(
                [[10.0, 10.0], [20.0, 20.0]],
                dtype=np.float32,
            )
            self._types = np.array([0, 1], dtype=np.int32)

        def update(self, _dt):
            self.update_calls += 1

        def get_positions(self):
            return self._positions

        def get_types(self):
            return self._types

    monkeypatch.setattr(viewer, "ParticleSystem", FakeSystem)
    monkeypatch.setattr(viewer.config, "WINDOW_WIDTH", 200)
    monkeypatch.setattr(viewer.config, "WINDOW_HEIGHT", 180)
    monkeypatch.setattr(viewer.config, "PARTICLE_COUNT", 2)
    monkeypatch.setattr(viewer.config, "SEED", None)

    first_batch = [
        viewer.pygame.event.Event(
            viewer.pygame.KEYDOWN,
            {"key": viewer.pygame.K_SPACE},
        ),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_f}),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_g}),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_r}),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_e}),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_t}),
        viewer.pygame.event.Event(viewer.pygame.KEYDOWN, {"key": viewer.pygame.K_z}),
        viewer.pygame.event.Event(
            viewer.pygame.MOUSEMOTION,
            {"pos": (12, 140)},
        ),
        viewer.pygame.event.Event(
            viewer.pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": (12, 140)},
        ),
        viewer.pygame.event.Event(viewer.pygame.QUIT, {}),
    ]
    event_batches = [first_batch, []]
    monkeypatch.setattr(
        viewer.pygame.event,
        "get",
        lambda: event_batches.pop(0) if event_batches else [],
    )
    monkeypatch.setattr(viewer.pygame.time, "Clock", FakeClock)

    with pytest.raises(SystemExit) as exc_info:
        viewer.run()

    assert exc_info.value.code == 0
