from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GameConfig:
    columns: int = 20
    rows: int = 18
    tile_size: int = 50
    hud_height: int = 100
    target_fps: int = 60
    start_speed: float = 7.0
    max_speed: float = 16.0
    speed_step: float = 0.35
    score_per_food: int = 5
    window_title: str = "basic snake game+"
    high_score_path: Path = Path("data/high_score.json")

    @property
    def board_width(self) -> int:
        return self.columns * self.tile_size

    @property
    def board_height(self) -> int:
        return self.rows * self.tile_size

    @property
    def window_size(self) -> tuple[int, int]:
        return self.board_width, self.board_height + self.hud_height
