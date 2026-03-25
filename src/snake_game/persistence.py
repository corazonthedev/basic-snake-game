from __future__ import annotations

import json
from pathlib import Path


def load_high_score(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data.get("high_score", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
        return 0


def save_high_score(path: Path, high_score: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"high_score": int(high_score)}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
