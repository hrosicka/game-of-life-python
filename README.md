# Game of Life — Python Edition

![Python](https://img.shields.io/badge/language-python-blue.svg)
![License](https://img.shields.io/github/license/hrosicka/game-of-life-python)
![Last Commit](https://img.shields.io/github/last-commit/hrosicka/game-of-life-python)
![GitHub stars](https://img.shields.io/github/stars/hrosicka/game-of-life-python?style=social)

Welcome to **Game of Life – Python Edition**, a visually engaging and educational implementation of Conway’s Game of Life. Here, you’ll find classic oscillator patterns rendered with modern terminal graphics, powered by Python and the [Rich](https://github.com/Textualize/rich) library. Explore mathematical beauty as cellular automata evolve before your eyes!

---

## ✨ Features

- **Classic oscillator simulations:**
  - **Pulsar:** A mesmerizing, large-period oscillator
  - **Toad:** The famous leaping two-phase pattern
  - **Beacon:** A “lonely lighthouse” blinking on the grid
  - **Blinker:** Simple and iconic three-cell line (available in its script)
- **Animated terminal graphics:** Smooth color rendering via [Rich](https://github.com/Textualize/rich)
- **Efficient computation:** Powered by [NumPy](https://numpy.org) and [SciPy](https://www.scipy.org) convolution for speedy generations
- **Modular, readable code:** Easily add your own patterns and tweaks
- **Friendly, instructive comments:** Code is easy to understand and modify

---

## 🗂️ Repository Structure

- `game-of-life-pulsar.py` — Simulates the Pulsar oscillator with wide grid and animated output
- `game-of-life-toad.py` — Runs the Toad pattern in a compact field
- `game-of-life-beacon.py` — Demonstrates the Beacon blinking behavior
- `game-of-life-blinker.py` — Classic Blinker in a smaller grid

Feel free to fork and add new patterns! The modular design makes extending simulations simple.

---

## ⚙️ Installation

**Requirements:**
- Python 3.8 or newer
- NumPy
- SciPy
- Rich

Install dependencies with pip:

```bash
pip install numpy scipy rich
```

---

## 🚦 Usage

Run any pattern simulation from your terminal:

```bash
python game-of-life-pulsar.py
python game-of-life-toad.py
python game-of-life-beacon.py
python game-of-life-blinker.py
```

Each script animates its classic pattern, updating the grid at set intervals. Use `Ctrl+C` to stop the simulation.

---

## 🧩 Add Your Own Pattern

1. Copy any existing script file (e.g., `game-of-life-toad.py`).
2. Change the pattern coordinates and grid sizing as desired.
3. Adjust comments and labels for clarity.
4. Share your creation with a pull request or fork!

---

## ℹ️ About Conway’s Game of Life

Conway’s Game of Life is a zero-player game—set the rules and observe endless emergent complexity! With simple laws governing cell birth and death, patterns emerge, oscillate, and sometimes surprise even mathematicians.

[Learn more about Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

---

## 🖼️ Visual Demos

> *Optional: Add screenshots or animated gifs here to showcase terminal graphics!*

---

## 📄 License

MIT License. This project is open for educational and entertainment use. Fork, share, and evolve it—your automata won’t judge!

---

## 🤝 Contributing

Pull requests, forks, suggestions, and feedback are encouraged. Make the code even more colorful and interesting by adding new patterns or improving existing ones.

---

*May your cells live long, oscillate often, and die interestingly!*