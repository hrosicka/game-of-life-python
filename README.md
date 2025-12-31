# Game of Life — Python Edition

![Python](https://img.shields.io/badge/language-python-blue.svg)
![License](https://img.shields.io/github/license/hrosicka/game-of-life-python)
![Last Commit](https://img.shields.io/github/last-commit/hrosicka/game-of-life-python)
![GitHub stars](https://img.shields.io/github/stars/hrosicka/game-of-life-python?style=social)

A set of small, focused Conway's Game of Life simulations implemented in Python. Each script runs a classic pattern (oscillators, gliders, Gosper glider gun, LWSS, etc.) and renders a live, animated view in the terminal using [Rich](https://github.com/Textualize/rich). Neighbor counting is implemented efficiently using 2D convolution via [SciPy](https://www.scipy.org) (or NumPy + SciPy).

This repository is intended to be:
- Educational: clear, simple code for studying Life rules and patterns.
- Visual: terminal-based live rendering with Rich.
- Extensible: add new patterns or tweak parameters by editing the scripts.

---

## Key implementation notes

- Rendering: uses Rich's live rendering (`rich.live.Live`) for smooth, colorful terminal output.
- Computation: uses `scipy.signal.convolve2d` to compute neighbor counts efficiently with small convolution kernels.
- Configuration: each script contains a `DEFAULT_CONFIG` dict (width, height, delay, characters) — edit these values in the script to change size, speed, and appearance.
- Exit: press `Ctrl+C` to stop any running simulation.
- Boundary handling:
  - Most scripts use toroidal wrap-around boundaries (`boundary='wrap'`) so the grid behaves like a donut (edges wrap).
  - The Gosper glider gun script uses non-wrapping / zero-filled boundary (`boundary='fill'`, `fillvalue=0`) to better match the classical presentation.

---

## Included scripts

- `game-of-life-pulsar.py` — Pulsar oscillator
  - Default config in the script: width 60, height 30, delay ~1.0s in the current main block.
  - Uses a full-block character for live cells (good for dense/large displays).
  - Places a Pulsar pattern via coordinate list and runs the simulation.

- `game-of-life-toad.py` — Toad oscillator
  - Typical config: width 30, height 15, delay 1.0s.
  - Uses two-character cell representation (`"o "` / `"  "`) for clearer spacing.

- `game-of-life-beacon.py` — Beacon oscillator (period 2)
  - Typical config: width 30, height 10, delay 1.0s.
  - Uses single-character live/dead representation.

- `game-of-life-blinker.py` — Blinker oscillator
  - Typical config: width 15, height 7, delay 0.5s.
  - Uses `"o "` / `"  "` style cells.

- `game-of-life-glider.py` — Glider patterns (several gliders)
  - Typical config: width 30, height 15, delay 0.5s.
  - Places two gliders and demonstrates toroidal wrap behavior.

- `game-of-life-gun.py` — Gosper Glider Gun
  - Typical config: width 100, height 40, low delay (e.g., 0.01s) for smooth glider motion.
  - Uses `boundary='fill'` (non-wrapping) so generated gliders travel across empty space.
  - Uses Rich Live with `screen=True` for an alternate buffer (full-screen-like display).

- `game-of-life-lwss.py` — Lightweight spaceship (LWSS) pattern
  - Implements the small ship pattern and renders it live (adjustable config inside the script).

- `tests/` — placeholder directory for tests (currently empty)

---

## Requirements

- Python 3.8+ (recommended)
- numpy
- scipy
- rich

Install dependencies with pip:

```bash
pip install numpy scipy rich
```

(If you plan to run the scripts inside virtualenv or venv, create and activate it first.)

---

## Usage

Run any script from your terminal. Example:

```bash
python game-of-life-pulsar.py
python game-of-life-toad.py
python game-of-life-beacon.py
python game-of-life-blinker.py
python game-of-life-glider.py
python game-of-life-gun.py
python game-of-life-lwss.py
```

Tips:
- If SciPy is not installed, each script prints an error message and exits (scripts check for `scipy.signal.convolve2d`).
- To change grid size, speed, or characters, edit the `DEFAULT_CONFIG` dictionary near the top of the script you want to change.
- For the Gosper Glider Gun script, `screen=True` is enabled for Live; if your terminal behaves oddly try removing `screen=True` in the `Live(...)` call.

---

## Extending / Adding patterns

1. Copy an existing script (e.g., `game-of-life-toad.py`) and rename it.
2. Update the pattern coordinates or create a new coordinate list for your pattern.
3. Adjust `DEFAULT_CONFIG` (width, height, delay, characters) if needed.
4. Run the script and observe the pattern.
5. If you'd like, open a PR to share new patterns.

---

## Troubleshooting

- Terminal rendering looks garbled:
  - Try a different font/terminal or adjust the cell character width in the script (some scripts use two-character cells like `"o "` for spacing).
  - If color/Unicode characters look off, change `live_cell_char`/`dead_cell_char` in the script to simpler ASCII characters.
- SciPy import error:
  - Install SciPy with `pip install scipy` (or `pip install numpy scipy`).
- Performance:
  - Very large grids with small delay may be CPU-heavy; increase `delay_seconds` or reduce grid size.
 
---
  
## About Conway’s Game of Life

Conway’s Game of Life is a zero-player game—set the rules and observe endless emergent complexity! With simple laws governing cell birth and death, patterns emerge, oscillate, and sometimes surprise even mathematicians.

[Learn more about Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

---

## Author

Lovingly crafted by [Hanka Robovska](https://github.com/hrosicka) 👩‍🔬

---

## License

MIT License. This project is open for educational and entertainment use.
