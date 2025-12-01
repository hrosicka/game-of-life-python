# Game of Life (Python Edition)

![Python](https://img.shields.io/badge/language-python-blue.svg)
![License](https://img.shields.io/github/license/hrosicka/game-of-life-python)
![Last Commit](https://img.shields.io/github/last-commit/hrosicka/game-of-life-python)
![GitHub stars](https://img.shields.io/github/stars/hrosicka/game-of-life-python?style=social)

Welcome to *yet another* take on Conway's Game of Life – because there are never enough ways to experience mathematical chaos (and because Python makes everything prettier). This repo provides several polished, terminal-based simulations of the famous zero-player game, using Python, SciPy, and Rich for smooth, colorful console output.

## ✨ Features

- Multiple classic oscillator patterns:
  - Pulsar (hypnotic and huge)
  - Toad (a true classic that leaps between two states)
  - Beacon (for when you want your cells to blink like a lonely lighthouse)
- Modern, animated terminal graphics thanks to [Rich](https://github.com/Textualize/rich)
- Blazing fast updates with [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/)
- Toggle configs, easy-to-read code, and a splash of personality

## 📂 Repository Structure

- `game-of-life-pulsar.py` – Simulates the epic Pulsar oscillator, with a wide grid and animated Rich output
- `game-of-life-toad.py` – Runs the Toad pattern, in a more compact field
- `game-of-life-beacon.py` – (Because sometimes you just want a blinking light!)

Feel free to add your own patterns – the code is modular and welcoming, like a friendly automaton.

## 🛠 Requirements

- Python 3.x
- `numpy`
- `scipy`
- `rich`

Install the dependencies:
```bash
pip install numpy scipy rich
```

## 🚀 Running the Simulations

Pick a pattern, then let it evolve:

```bash
python game-of-life-pulsar.py
python game-of-life-toad.py
python game-of-life-beacon.py
```

Watch your terminal come alive! Each script shows pattern evolution step by step (press `Ctrl+C` for the circle of life to end).

## ℹ️ About Conway's Game of Life

Conway's Game of Life is a grid-based, zero-player game where you define the rules and the universe does the rest. Simple laws; infinite weirdness. Still no actual frogs or beacons, though.

## 📖 License

MIT License unless stated otherwise. This project is for educational and entertainment purposes. Fork, modify, or break as you wish — the automata won’t judge you!

---
*May your cells live long, oscillate often, and die interestingly.*