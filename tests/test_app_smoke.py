from snake_game.app import run


def test_app_runs_headless_for_a_few_frames(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    score = run(max_frames=5, headless=True, seed=4)
    assert isinstance(score, int)
