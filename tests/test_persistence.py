from pathlib import Path

from snake_game.persistence import load_high_score, save_high_score


def test_high_score_roundtrip(tmp_path: Path) -> None:
    score_path = tmp_path / "high_score.json"
    assert load_high_score(score_path) == 0
    save_high_score(score_path, 55)
    assert load_high_score(score_path) == 55
