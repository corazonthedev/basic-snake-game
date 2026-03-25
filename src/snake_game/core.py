from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import Iterable

from .config import GameConfig


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> "Point":
        dx, dy = other
        return Point(self.x + dx, self.y + dy)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> tuple[int, int]:
        return self.value

    def is_opposite(self, other: "Direction | None") -> bool:
        if other is None:
            return False
        dx, dy = self.vector
        ox, oy = other.vector
        return dx == -ox and dy == -oy


class GameState(Enum):
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"


@dataclass(frozen=True, slots=True)
class StepResult:
    ate_food: bool = False
    crashed: bool = False
    score_changed: bool = False


class SnakeGame:
    def __init__(self, config: GameConfig | None = None, seed: int | None = None) -> None:
        self.config = config or GameConfig()
        self._rng = random.Random(seed)
        self.best_score = 0
        self.reset()

    def reset(self) -> None:
        center = Point(self.config.columns // 2, self.config.rows // 2)
        self.snake: list[Point] = [center, Point(center.x - 1, center.y), Point(center.x - 2, center.y)]
        self.direction = Direction.RIGHT
        self.pending_direction: Direction | None = self.direction
        self.state = GameState.READY
        self.score = 0
        self.food = self._spawn_food()

    @property
    def speed(self) -> float:
        return min(
            self.config.start_speed + max(len(self.snake) - 3, 0) * self.config.speed_step,
            self.config.max_speed,
        )

    def start(self) -> None:
        if self.state in {GameState.READY, GameState.GAME_OVER}:
            if self.state == GameState.GAME_OVER:
                self.reset()
            self.state = GameState.RUNNING

    def restart(self) -> None:
        self.reset()
        self.state = GameState.RUNNING

    def toggle_pause(self) -> None:
        if self.state == GameState.RUNNING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.RUNNING

    def queue_direction(self, direction: Direction) -> None:
        current = self.pending_direction or self.direction
        if direction.is_opposite(current):
            return
        self.pending_direction = direction
        if self.state == GameState.READY:
            self.state = GameState.RUNNING

    def step(self) -> StepResult:
        if self.state != GameState.RUNNING:
            return StepResult()

        if self.pending_direction is not None:
            self.direction = self.pending_direction

        next_head = self.snake[0] + self.direction.vector
        if self._hits_wall(next_head) or next_head in self.snake[:-1]:
            self.state = GameState.GAME_OVER
            self.best_score = max(self.best_score, self.score)
            return StepResult(crashed=True)

        ate_food = next_head == self.food
        self.snake.insert(0, next_head)

        if ate_food:
            self.score += self.config.score_per_food
            self.best_score = max(self.best_score, self.score)
            self.food = self._spawn_food(exclude=self.snake)
            return StepResult(ate_food=True, score_changed=True)

        self.snake.pop()
        return StepResult()

    def _hits_wall(self, point: Point) -> bool:
        return not (0 <= point.x < self.config.columns and 0 <= point.y < self.config.rows)

    def _spawn_food(self, exclude: Iterable[Point] | None = None) -> Point:
        blocked = set(exclude or self.snake)
        free_tiles = [
            Point(x, y)
            for x in range(self.config.columns)
            for y in range(self.config.rows)
            if Point(x, y) not in blocked
        ]
        return self._rng.choice(free_tiles)
