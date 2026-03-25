from snake_game.config import GameConfig
from snake_game.core import Direction, GameState, Point, SnakeGame


def make_game() -> SnakeGame:
    return SnakeGame(config=GameConfig(columns=8, rows=8, tile_size=20, hud_height=40), seed=2)


def test_initial_state_is_ready_and_valid() -> None:
    game = make_game()
    assert game.state == GameState.READY
    assert len(game.snake) == 3
    assert game.food not in game.snake


def test_reverse_direction_is_ignored() -> None:
    game = make_game()
    game.queue_direction(Direction.LEFT)
    assert game.pending_direction == Direction.RIGHT


def test_eating_food_increases_score_and_length() -> None:
    game = make_game()
    game.start()
    game.food = Point(game.snake[0].x + 1, game.snake[0].y)
    result = game.step()
    assert result.ate_food is True
    assert game.score == game.config.score_per_food
    assert len(game.snake) == 4


def test_wall_collision_ends_game() -> None:
    game = make_game()
    game.start()
    game.snake = [Point(7, 2), Point(6, 2), Point(5, 2)]
    game.direction = Direction.RIGHT
    game.pending_direction = Direction.RIGHT
    result = game.step()
    assert result.crashed is True
    assert game.state == GameState.GAME_OVER


def test_pause_stops_progress() -> None:
    game = make_game()
    game.start()
    initial_snake = list(game.snake)
    game.toggle_pause()
    game.step()
    assert game.snake == initial_snake
    assert game.state == GameState.PAUSED


def test_restart_resets_board_and_state() -> None:
    game = make_game()
    game.start()
    game.food = Point(game.snake[0].x + 1, game.snake[0].y)
    game.step()
    game.restart()
    assert game.state == GameState.RUNNING
    assert game.score == 0
    assert len(game.snake) == 3
