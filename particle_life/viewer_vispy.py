"""
Vispy-based viewer for particle life simulation.

Uses OpenGL via Vispy for better performance than Pygame,
especially with many particles (>1000).

PoC - Run directly for static test points:
    python particle_life/viewer_vispy.py

Integration - Run via main.py with real simulation:
    python particle_life/main.py --mode vispy
"""

import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np

# Dependency Setup
try:
    import particle_life.config as config
    from particle_life.simulation import ParticleSystem
except ModuleNotFoundError:
    root_dir = Path(__file__).resolve().parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))
    import particle_life.config as config
    from particle_life.simulation import ParticleSystem

from vispy import app, scene


def _build_color_array(types: np.ndarray) -> np.ndarray:
    """
    Convert particle types to RGBA color array.

    Takes RGB tuples (0-255) from config.COLOR_PALETTE and creates a
    (N, 4) float32 array with values 0.0-1.0 for Vispy.
    """
    palette_rgba = np.array(
        [
            (r / 255.0, g / 255.0, b / 255.0, 1.0)
            for r, g, b in config.COLOR_PALETTE
        ],
        dtype=np.float32,
    )
    color_indices = types % len(config.COLOR_PALETTE)
    return palette_rgba[color_indices]


class VispyViewer:
    """OpenGL-based particle viewer using Vispy SceneCanvas."""

    def __init__(
        self,
        sim: Optional[ParticleSystem] = None,
    ) -> None:
        """
        Initialize the viewer.

        Args:
            sim: ParticleSystem instance. If None, starts PoC mode
                 with random static points (Issue #35).
        """
        self.sim = sim
        self.is_poc = sim is None
        self.paused = False

        # Canvas & View
        self.canvas = scene.SceneCanvas(
            title=config.TITLE if not self.is_poc else "Vispy PoC – Statische Punkte",
            size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            bgcolor=tuple(c / 255.0 for c in config.BACKGROUND_COLOR),
            keys="interactive",
            show=True,
        )
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(aspect=1)
        self.view.camera.set_range(
            x=(0, config.WINDOW_WIDTH),
            y=(0, config.WINDOW_HEIGHT),
        )

        # Markers Visual
        self.markers = scene.visuals.Markers(parent=self.view.scene)

        # Info-Text Overlay
        self.info_text = scene.visuals.Text(
            text="",
            color="white",
            font_size=10,
            anchor_x="left",
            anchor_y="top",
            parent=self.canvas.scene,
        )
        self.info_text.pos = (10, 18)

        # Control help text at bottom
        self.help_text = scene.visuals.Text(
            text="[Space] Pause  [F/G] Friction ±  [R/E] Force ±  [T/Z] Radius ±",
            color=(0.6, 0.6, 0.6, 1.0),
            font_size=9,
            anchor_x="left",
            anchor_y="bottom",
            parent=self.canvas.scene,
        )
        self.help_text.pos = (10, config.WINDOW_HEIGHT - 10)

        if self.is_poc:
            # Static random points
            n = config.PARTICLE_COUNT
            positions = np.random.rand(n, 2).astype(np.float32)
            positions[:, 0] *= config.WINDOW_WIDTH
            positions[:, 1] *= config.WINDOW_HEIGHT
            random_types = np.random.randint(
                0, config.PARTICLE_TYPES, size=n, dtype=np.int32
            )
            colors = _build_color_array(random_types)
            self.markers.set_data(
                pos=positions,
                face_color=colors,
                size=4,
                edge_width=0,
            )
            self.info_text.text = f"PoC Mode  |  {n} points (static)"
        else:
            # Real simulation - set initial data
            self.colors = _build_color_array(self.sim.get_types())
            self.markers.set_data(
                pos=self.sim.get_positions(),
                face_color=self.colors,
                size=4,
                edge_width=0,
            )

            # Timer for the update loop (~60 FPS)
            self._frame_count = 0
            self._last_fps_time = time.perf_counter()
            self._fps = 0.0
            self._step = 0

            self.timer = app.Timer(
                interval=1.0 / 60.0,
                connect=self._on_timer,
                start=True,
            )

        # Keyboard events
        self.canvas.events.key_press.connect(self._on_key_press)

    def _update_info_text(self) -> None:
        """Update the info display in top left corner."""
        mode_text = "PAUSED" if self.paused else "running"
        self.info_text.text = (
            f"step={self._step}  fps={self._fps:.0f}  "
            f"friction={self.sim.friction:.3f}  "
            f"force={config.FORCE_FACTOR:.2f}  "
            f"radius={config.MAX_RADIUS:.1f}  "
            f"mode={mode_text}"
        )

    def _on_timer(self, event) -> None:
        """Called by Vispy timer: updates the simulation."""
        if not self.paused:
            self.sim.update(config.DT)
            self._step += 1

        self.markers.set_data(
            pos=self.sim.get_positions(),
            face_color=self.colors,
            size=4,
            edge_width=0,
        )

        # FPS berechnen
        self._frame_count += 1
        now = time.perf_counter()
        elapsed = now - self._last_fps_time
        if elapsed >= 1.0:
            self._fps = self._frame_count / elapsed
            self._frame_count = 0
            self._last_fps_time = now
            self.canvas.title = (
                f"{config.TITLE}  |  "
                f"FPS: {self._fps:.0f}  |  "
                f"Partikel: {self.sim.n_particles}"
            )

        self._update_info_text()

    def _on_key_press(self, event) -> None:
        """
        Keyboard control (same keys as Pygame viewer):
          Space = Pause/Play
          F/G   = Friction +/-
          R/E   = Force +/-
          T/Z   = Radius +/-
          ESC   = Close window
        """
        if event.key == "Escape":
            self.canvas.close()
            app.quit()

        # Restliche Tasten nur im Simulations-Modus
        if self.is_poc:
            return

        if event.key == " ":
            self.paused = not self.paused
        elif event.key == "F":
            self.sim.friction = float(min(max(self.sim.friction + 0.01, 0.0), 1.0))
        elif event.key == "G":
            self.sim.friction = float(min(max(self.sim.friction - 0.01, 0.0), 1.0))
        elif event.key == "R":
            config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 1.1, 0.0))
        elif event.key == "E":
            config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 0.9, 0.0))
        elif event.key == "T":
            config.MAX_RADIUS = float(max(config.MAX_RADIUS + 1.0, 0.0))
        elif event.key == "Z":
            config.MAX_RADIUS = float(max(config.MAX_RADIUS - 1.0, 0.0))

        self._update_info_text()


def run() -> None:
    """Start the Vispy viewer with real simulation."""
    if config.SEED is not None:
        np.random.seed(config.SEED)

    sim = ParticleSystem()
    _viewer = VispyViewer(sim=sim)  # noqa: F841: Referenz halten
    app.run()


def run_poc() -> None:
    """Start PoC mode with random static points (Issue #35)."""
    _viewer = VispyViewer(sim=None)  # noqa: F841: Referenz halten
    app.run()


if __name__ == "__main__":
    # Direkt ausführen = PoC Modus (Issue #35)
    run_poc()
