import sys
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import pygame


def _import_dependencies():
    try:
        import particle_life.config as config
        from particle_life.simulation import ParticleSystem
        return config, ParticleSystem
    except ModuleNotFoundError:
        root_dir = Path(__file__).resolve().parent.parent
        if str(root_dir) not in sys.path:
            sys.path.insert(0, str(root_dir))
        import particle_life.config as config
        from particle_life.simulation import ParticleSystem
        return config, ParticleSystem


config, ParticleSystem = _import_dependencies()


class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        callback: Callable[[], None],
        base_color: tuple[int, int, int],
        hover_color: tuple[int, int, int],
        text_color: tuple[int, int, int],
        dynamic_text: Optional[Callable[[], str]] = None,
    ) -> None:
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        self.dynamic_text = dynamic_text

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(surface, color, self.rect)
        label = self.dynamic_text() if self.dynamic_text is not None else self.text
        text_surface = self.font.render(label, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback()

def run() -> None:
    if config.SEED is not None:
        np.random.seed(config.SEED)

    pygame.init()
    screen = pygame.display.set_mode(
        (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    )
    pygame.display.set_caption(config.TITLE)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    sim = ParticleSystem()
    running = True
    paused = False
    step = 0

    def toggle_pause() -> None:
        nonlocal paused
        paused = not paused

    def increase_friction() -> None:
        sim.friction = float(min(max(sim.friction + 0.01, 0.0), 1.0))

    def decrease_friction() -> None:
        sim.friction = float(min(max(sim.friction - 0.01, 0.0), 1.0))

    def increase_force() -> None:
        config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 1.1, 0.0))

    def decrease_force() -> None:
        config.FORCE_FACTOR = float(max(config.FORCE_FACTOR * 0.9, 0.0))

    def increase_radius() -> None:
        config.MAX_RADIUS = float(max(config.MAX_RADIUS + 1.0, 0.0))

    def decrease_radius() -> None:
        config.MAX_RADIUS = float(max(config.MAX_RADIUS - 1.0, 0.0))

    panel_height = 60
    panel_y = config.WINDOW_HEIGHT - panel_height
    button_width = 120
    button_height = 36
    button_margin = 10
    base_color = (60, 60, 60)
    hover_color = (100, 100, 100)
    text_color = (255, 255, 255)

    buttons: list[Button] = []
    x = 10

    pause_button = Button(
        pygame.Rect(x, panel_y + 12, button_width, button_height),
        "Pause",
        font,
        toggle_pause,
        base_color,
        hover_color,
        text_color,
        dynamic_text=lambda: "Play" if paused else "Pause",
    )
    buttons.append(pause_button)
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Friction +",
            font,
            increase_friction,
            base_color,
            hover_color,
            text_color,
        )
    )
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Friction -",
            font,
            decrease_friction,
            base_color,
            hover_color,
            text_color,
        )
    )
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Force +",
            font,
            increase_force,
            base_color,
            hover_color,
            text_color,
        )
    )
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Force -",
            font,
            decrease_force,
            base_color,
            hover_color,
            text_color,
        )
    )
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Radius +",
            font,
            increase_radius,
            base_color,
            hover_color,
            text_color,
        )
    )
    x += button_width + button_margin

    buttons.append(
        Button(
            pygame.Rect(x, panel_y + 12, button_width, button_height),
            "Radius -",
            font,
            decrease_radius,
            base_color,
            hover_color,
            text_color,
        )
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    toggle_pause()
                elif event.key == pygame.K_f:
                    increase_friction()
                elif event.key == pygame.K_g:
                    decrease_friction()
                elif event.key == pygame.K_r:
                    increase_force()
                elif event.key == pygame.K_e:
                    decrease_force()
                elif event.key == pygame.K_t:
                    increase_radius()
                elif event.key == pygame.K_z:
                    decrease_radius()
            for button in buttons:
                button.handle_event(event)

        if not paused:
            sim.update(config.DT)
        positions = sim.get_positions()
        types = sim.get_types()

        screen.fill(config.BACKGROUND_COLOR)

        radius = 2
        for i in range(len(positions)):
            x_pos = int(positions[i, 0])
            y_pos = int(positions[i, 1])
            t = int(types[i])
            color_index = t % len(config.COLOR_PALETTE)
            color = config.COLOR_PALETTE[color_index]
            pygame.draw.circle(screen, color, (x_pos, y_pos), radius)

        fps = clock.get_fps()
        mode_text = "paused" if paused else "running"
        info = (
            f"step={step} fps={fps:.1f} "
            f"friction={sim.friction:.3f} "
            f"force={config.FORCE_FACTOR:.2f} "
            f"radius={config.MAX_RADIUS:.1f} "
            f"mode={mode_text}"
        )
        text_surface = font.render(info, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
        pygame.draw.rect(
            screen,
            (30, 30, 30),
            pygame.Rect(
                0,
                panel_y,
                config.WINDOW_WIDTH,
                panel_height,
            ),
        )
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        step += 1

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
