<div align="center">

# Basic Snake Game+

A polished remake of a minimal snake game — rebuilt with a cleaner architecture, better UX, persistent high scores, and automated tests while keeping the original arcade feel.

<p>
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/pygame-2.x-0A0A0A?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame 2.x" />
  <img src="https://img.shields.io/badge/tests-pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/status-ready%20to%20play-2EA44F?style=for-the-badge" alt="Ready to play" />
</p>

</div>

---

## Overview

This project started as a very small single-file snake game.
It has been refactored into a more maintainable and testable codebase without losing the simple green-grid / red-food identity that made the original version work.

The result is a repo that feels better to play, easier to read, and much safer to extend.

## Features

- Clean, modular architecture instead of one large script
- Improved in-game flow: start, pause, restart, and game-over states
- Persistent high score stored locally
- Support for both **WASD** and **Arrow Keys**
- Headless smoke testing for safer CI runs
- GitHub Actions workflow for automated validation
- Legacy launcher compatibility preserved through both entrypoints:
  - `main.py`
  - `basic snake game.py`

## Why this version is better

This remake keeps the original vibe, but fixes the parts that usually make tiny game repos hard to maintain:

- gameplay logic is separated from rendering
- persistence is separated from UI code
- configuration lives in one place
- tests protect the core mechanics
- the repo is structured like a real project, not a throwaway script

## Quick Start

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd basic-snake-game
```

### 2) Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### 4) Run the game

```bash
python main.py
```

You can also run the legacy entry file:

```bash
python "basic snake game.py"
```

## Controls

| Key | Action |
| --- | --- |
| `WASD` / `Arrow Keys` | Move the snake |
| `Space` / `Enter` | Start or play again |
| `Esc` | Pause / resume |
| `R` | Restart instantly |
| `Q` | Quit |

## Testing

Run the full test suite:

```bash
pytest
```

For fully headless environments (CI, remote shell, container):

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy pytest
```

## Project Structure

```text
basic-snake-game/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── .gitkeep
├── docs/
│   └── ADR.md
├── src/
│   └── snake_game/
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── core.py
│       └── persistence.py
├── tests/
│   ├── test_app_smoke.py
│   ├── test_core.py
│   └── test_persistence.py
├── basic snake game.py
├── main.py
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── README.md
```

## Architecture

### `src/snake_game/core.py`
Pure gameplay rules:
- snake movement
- collision checks
- food spawning
- score handling
- state transitions

### `src/snake_game/app.py`
Pygame layer:
- input handling
- rendering
- overlays / HUD
- runtime loop

### `src/snake_game/persistence.py`
Small persistence layer for loading and saving the best score.

### `src/snake_game/config.py`
Central game settings such as grid size, speed, tile size, and window title.

## Design Goals

This project is intentionally built around a few simple rules:

1. **Keep the original feel**
2. **Improve readability without overengineering**
3. **Make future changes safer through tests**
4. **Ship a cleaner UI/UX without losing the arcade simplicity**

## Contributing

If you want to improve the project:

1. Fork the repo
2. Create a feature branch
3. Run tests before opening a PR
4. Keep changes focused and small

More detail: see [CONTRIBUTING.md](CONTRIBUTING.md)

## Development Notes

- High score data is stored locally inside the `data/` directory
- The project is configured through `pyproject.toml`
- CI is set up to run the automated tests on push / pull request

## License

This repository currently follows the structure of the original uploaded project.
If you want a formal open-source license, add one explicitly before publishing.

---

<div align="center">

**Built to feel simple. Structured to scale better.**

</div>
