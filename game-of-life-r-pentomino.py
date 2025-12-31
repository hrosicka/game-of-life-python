#!/usr/bin/env python3
"""
Conway's Game of Life: R-pentomino Evolution
Optimized for terminal performance using NumPy/SciPy and Rich.
"""

import time
import sys
from dataclasses import dataclass
from typing import Tuple, List, Optional

import numpy as np
from rich.live import Live
from rich.console import Console
from rich.text import Text

# Try-except block is moved to the top for immediate dependency check
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: Missing dependency 'scipy'. Install via 'pip install scipy'.")
    sys.exit(1)

@dataclass
class GameConfig:
    """Configuration schema for the Game of Life simulation."""
    width: int = 120
    height: int = 60
    delay_seconds: float = 0.03
    live_char: str = "█"
    dead_char: str = " "
    boundary: str = "fill"  # Options: 'fill' (constant 0) or 'wrap' (toroidal)

class GameOfLife:
    """
    Manages the core simulation logic and state for Conway's Game of Life.
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        Initialize the simulation with a grid of zeros.
        
        Args:
            config: An optional GameConfig instance. Defaults to standard values.
        """
        self.cfg = config or GameConfig()
        self.grid = np.zeros((self.cfg.height, self.cfg.width), dtype=np.int8)
        self.generation = 0
        self.console = Console()
        
        # Pre-compute convolution kernel for neighborhood counting
        self._kernel = np.array([[1, 1, 1],
                                 [1, 0, 1],
                                 [1, 1, 1]], dtype=np.int8)

    def seed_pattern(self, pattern: List[Tuple[int, int]], row_offset: int, col_offset: int):
        """
        Seeds a specific coordinate pattern into the grid.
        
        Args:
            pattern: List of (row, col) relative coordinates.
            row_offset: Vertical starting position.
            col_offset: Horizontal starting position.
        """
        for r, c in pattern:
            target_r, target_c = r + row_offset, c + col_offset
            if 0 <= target_r < self.cfg.height and 0 <= target_c < self.cfg.width:
                self.grid[target_r, target_c] = 1

    def setup_r_pentomino(self):
        """Initializes the R-pentomino pattern in the center of the grid."""
        r_pentomino = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]
        
        # Calculate center coordinates
        center_r = self.cfg.height // 2 - 1
        center_c = self.cfg.width // 2 - 1
        self.seed_pattern(r_pentomino, center_r, center_c)

    def _get_neighbor_counts(self) -> np.ndarray:
        """Counts neighbors using high-performance 2D convolution."""
        return convolve2d(
            self.grid, 
            self._kernel, 
            mode='same', 
            boundary=self.cfg.boundary
        ).astype(np.int8)

    def step(self):
        """Calculates and applies the next generation based on B3/S23 rules."""
        neighbors = self._get_neighbor_counts()
        
        # Survival: live cell with 2 or 3 neighbors
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        # Birth: dead cell with exactly 3 neighbors
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def render(self) -> Text:
        """
        Converts the current grid state into a formatted Rich Text object.
        Uses NumPy vectorization for character mapping.
        """
        # Vectorized mapping of cells to characters for speed
        chars = np.where(self.grid == 1, self.cfg.live_char, self.cfg.dead_char)
        rows = ["".join(row) for row in chars]
        
        header = f"[bold white]Generation:[/bold white] {self.generation} | " \
                 f"[bold white]Boundary:[/bold white] {self.cfg.boundary}\n"
        content = "\n".join(rows)
        footer = "\n[dim italic]Press Ctrl+C to terminate simulation[/dim italic]"
        
        return Text.from_markup(header) + Text(content, style="green") + Text.from_markup(footer)

    def run(self):
        """Executes the simulation loop with live terminal updates."""
        self.console.clear()
        self.console.print("[bold blue]Initialising R-pentomino...[/bold blue]")
        time.sleep(1)

        try:
            with Live(self.render(), console=self.console, screen=True, auto_refresh=False) as live:
                while True:
                    live.update(self.render(), refresh=True)
                    self.step()
                    time.sleep(self.cfg.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Simulation terminated by user.[/bold yellow]")
        except Exception as e:
            self.console.print(f"\n[bold red]Runtime Error:[/bold red] {e}")

if __name__ == "__main__":
    # Example: Override default dimensions via config dataclass
    config = GameConfig(width=120, height=60)
    
    simulation = GameOfLife(config)
    simulation.setup_r_pentomino()
    simulation.run();