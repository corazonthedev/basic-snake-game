from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pygame

from .config import GameConfig
from .core import Direction, GameState, Point, SnakeGame
from .persistence import load_high_score, save_high_score

Color = tuple[int, int, int]

BACKGROUND_LIGHT: Color = (152, 251, 152)
BACKGROUND_DARK: Color = (34, 115, 62)
HUD_BG: Color = (18, 20, 24)
PANEL_BG: Color = (247, 166, 0)
PANEL_BORDER: Color = (255, 227, 147)
SNAKE_HEAD: Color = (25, 25, 25)
SNAKE_BODY: Color = (110, 110, 110)
FOOD: Color = (219, 48, 48)
WHITE: Color = (250, 250, 250)
BLACK: Color = (0, 0, 0)
MUTED: Color = (210, 215, 220)
SHADOW: Color = (70, 70, 70)

KEY_TO_DIRECTION = {
    pygame.K_w: Direction.UP,
    pygame.K_UP: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_a: Direction.LEFT,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_d: Direction.RIGHT,
    pygame.K_RIGHT: Direction.RIGHT,
}


def _resource_path(path: Path) -> Path:
    return path if path.is_absolute() else Path.cwd() / path


def _draw_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: Color,
    position: tuple[int, int],
    *,
    center: bool = False,
) -> pygame.Rect:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=position) if center else rendered.get_rect(topleft=position)
    surface.blit(rendered, rect)
    return rect


def _draw_overlay(screen: pygame.Surface, rect: pygame.Rect) -> None:
    shadow = rect.move(10, 12)
    pygame.draw.rect(screen, SHADOW, shadow, border_radius=26)
    pygame.draw.rect(screen, PANEL_BG, rect, border_radius=26)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=4, border_radius=26)


def _draw_checkerboard(screen: pygame.Surface, config: GameConfig) -> None:
    for x in range(config.columns):
        for y in range(config.rows):
            color = BACKGROUND_LIGHT if (x + y) % 2 == 0 else BACKGROUND_DARK
            rect = pygame.Rect(
                x * config.tile_size,
                config.hud_height + y * config.tile_size,
                config.tile_size,
                config.tile_size,
            )
            pygame.draw.rect(screen, color, rect)


def _tile_rect(point: Point, config: GameConfig, shrink: int = 4) -> pygame.Rect:
    return pygame.Rect(
        point.x * config.tile_size + shrink // 2,
        config.hud_height + point.y * config.tile_size + shrink // 2,
        config.tile_size - shrink,
        config.tile_size - shrink,
    )


def _draw_hud(screen: pygame.Surface, game: SnakeGame, config: GameConfig, hud_font: pygame.font.Font) -> None:
    pygame.draw.rect(screen, HUD_BG, (0, 0, config.board_width, config.hud_height))
    _draw_text(screen, hud_font, f"score  {game.score}", WHITE, (24, 24))
    _draw_text(
        screen,
        hud_font,
        f"best  {game.best_score}",
        WHITE,
        (config.board_width - 220, 24),
    )
    _draw_text(screen, hud_font, f"speed  {game.speed:.1f}", MUTED, (24, 56))
    help_text = "WASD / arrows move   ESC pause   R restart"
    _draw_text(screen, hud_font, help_text, MUTED, (config.board_width - 430, 56))


def _draw_snake(screen: pygame.Surface, game: SnakeGame, config: GameConfig) -> None:
    food_rect = _tile_rect(game.food, config, shrink=8)
    pygame.draw.ellipse(screen, FOOD, food_rect)
    pygame.draw.ellipse(screen, WHITE, food_rect.inflate(-18, -18))

    for index, segment in enumerate(reversed(game.snake)):
        is_head = index == len(game.snake) - 1
        color = SNAKE_HEAD if is_head else SNAKE_BODY
        rect = _tile_rect(segment, config)
        pygame.draw.rect(screen, color, rect, border_radius=12)


def _draw_start_panel(screen: pygame.Surface, config: GameConfig, title_font: pygame.font.Font, body_font: pygame.font.Font) -> None:
    panel = pygame.Rect(150, 220, config.board_width - 300, 360)
    _draw_overlay(screen, panel)
    _draw_text(screen, title_font, "basic snake game+", BLACK, (config.board_width // 2, 310), center=True)
    _draw_text(screen, body_font, "Same simple snake feel, cleaner UI, better flow.", BLACK, (config.board_width // 2, 390), center=True)
    _draw_text(screen, body_font, "SPACE to start  •  WASD / arrows to move", BLACK, (config.board_width // 2, 450), center=True)
    _draw_text(screen, body_font, "ESC pauses  •  R restarts", BLACK, (config.board_width // 2, 495), center=True)


def _draw_pause_panel(screen: pygame.Surface, config: GameConfig, title_font: pygame.font.Font, body_font: pygame.font.Font) -> None:
    panel = pygame.Rect(220, 250, config.board_width - 440, 270)
    _draw_overlay(screen, panel)
    _draw_text(screen, title_font, "paused", BLACK, (config.board_width // 2, 325), center=True)
    _draw_text(screen, body_font, "ESC to continue", BLACK, (config.board_width // 2, 400), center=True)
    _draw_text(screen, body_font, "R to restart  •  Q to quit", BLACK, (config.board_width // 2, 445), center=True)


def _draw_game_over_panel(
    screen: pygame.Surface,
    game: SnakeGame,
    config: GameConfig,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    panel = pygame.Rect(185, 220, config.board_width - 370, 340)
    _draw_overlay(screen, panel)
    _draw_text(screen, title_font, "eliminated!", (170, 0, 0), (config.board_width // 2, 305), center=True)
    _draw_text(screen, body_font, f"final score: {game.score}", BLACK, (config.board_width // 2, 390), center=True)
    _draw_text(screen, body_font, f"best score: {game.best_score}", BLACK, (config.board_width // 2, 435), center=True)
    _draw_text(screen, body_font, "SPACE to play again  •  Q to quit", BLACK, (config.board_width // 2, 490), center=True)


def _render(
    screen: pygame.Surface,
    game: SnakeGame,
    config: GameConfig,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
    hud_font: pygame.font.Font,
) -> None:
    _draw_checkerboard(screen, config)
    _draw_hud(screen, game, config, hud_font)
    _draw_snake(screen, game, config)

    if game.state == GameState.READY:
        _draw_start_panel(screen, config, title_font, body_font)
    elif game.state == GameState.PAUSED:
        _draw_pause_panel(screen, config, title_font, body_font)
    elif game.state == GameState.GAME_OVER:
        _draw_game_over_panel(screen, game, config, title_font, body_font)

    pygame.display.flip()


def _handle_key(game: SnakeGame, event_key: int) -> bool:
    if event_key in KEY_TO_DIRECTION:
        game.queue_direction(KEY_TO_DIRECTION[event_key])
        return False
    if event_key == pygame.K_ESCAPE:
        if game.state == GameState.READY:
            return True
        game.toggle_pause()
        return False
    if event_key == pygame.K_r:
        game.restart()
        return False
    if event_key in {pygame.K_SPACE, pygame.K_RETURN}:
        game.start()
        return False
    if event_key == pygame.K_q:
        return True
    return False


def run(*, max_frames: int | None = None, headless: bool = False, seed: int | None = None) -> int:
    if headless:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    pygame.init()
    config = GameConfig()
    game = SnakeGame(config=config, seed=seed)
    score_path = _resource_path(config.high_score_path)
    game.best_score = load_high_score(score_path)

    screen = pygame.display.set_mode(config.window_size)
    pygame.display.set_caption(config.window_title)
    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 68)
    body_font = pygame.font.Font(None, 34)
    hud_font = pygame.font.Font(None, 28)

    move_timer = 0.0
    frames = 0
    should_quit = False

    while not should_quit:
        delta = clock.tick(config.target_fps) / 1000
        move_timer += delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                should_quit = _handle_key(game, event.key)

        if game.state == GameState.RUNNING and move_timer >= 1 / game.speed:
            move_timer = 0.0
            game.step()
            save_high_score(score_path, game.best_score)

        _render(screen, game, config, title_font, body_font, hud_font)

        frames += 1
        if max_frames is not None and frames >= max_frames:
            break

    save_high_score(score_path, game.best_score)
    pygame.quit()
    return game.best_score


if __name__ == "__main__":
    run()
