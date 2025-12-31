#!/usr/bin/env python3
"""
Game of Life — R-pentomino pattern

The R-pentomino is a small 5-cell seed that leads to a very rich and 
long-lasting evolution (1103 generations to stabilize).
"""

import time
import sys
from typing import Dict, Any, Optional, Tuple, List

import numpy as np

try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy is required (pip install scipy).")
    sys.exit(1)

from rich.live import Live
from rich.console import Console
from rich.text import Text

class RPentominoGame:
    """
    Simulates Conway's Game of Life with an R-pentomino starter.
    """
    
    # Increased default size as R-pentomino expands significantly
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 120,
        "height": 60,
        "delay_seconds": 0.03,
        "live_cell_char": "█",
        "dead_cell_char": " ",
        "boundary": "fill"  # 'fill' (dead borders) or 'wrap' (toroidal)
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize grid, configuration and console."""
        self.cfg = {**self.DEFAULT_CONFIG, **(config or {})}
        
        self.width = int(self.cfg["width"])
        self.height = int(self.cfg["height"])
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0
        self.console = Console()

    def set_initial_pattern(self, pattern: List[Tuple[int, int]], offset_r: int, offset_c: int):
        """Sets initial live cells based on coordinates and offsets."""
        for r, c in pattern:
            rr, cc = r + offset_r, c + offset_c
            if 0 <= rr < self.height and 0 <= cc < self.width:
                self.grid[rr, cc] = 1

    def setup_r_pentomino(self):
        """Places the R-pentomino pattern in the center of the grid."""
        # Pattern shape:
        #  . X X
        #  X X .
        #  . X .
        r_pentomino = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]
        
        center_r = self.height // 2 - 1
        center_c = self.width // 2 - 1
        self.set_initial_pattern(r_pentomino, center_r, center_c)

    def generate_frame(self) -> Text:
        """Creates a Rich Text representation for display."""
        header = f"Gen: {self.generation} | Size: {self.width}x{self.height} | Boundary: {self.cfg['boundary']}\n"
        
        # Efficiently build the grid string using join on each row
        rows = [
            "".join(self.cfg["live_cell_char"] if cell else self.cfg["dead_cell_char"] for cell in row)
            for row in self.grid
        ]
        
        footer = "\nPress Ctrl+C to exit"
        return Text(header + "\n".join(rows) + footer, style="green")

    def _count_neighbors(self) -> np.ndarray:
        """Calculates neighbor count using 2D convolution."""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        return convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary=self.cfg['boundary']
        ).astype(np.int8)

    def update_grid(self):
        """Applies Conway's rules to calculate the next generation."""
        neighbors = self._count_neighbors()
        
        # Rules: 
        # 1. Survival: Live cell with 2 or 3 neighbors stays alive
        # 2. Birth: Dead cell with exactly 3 neighbors becomes alive
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Main simulation loop with live rendering."""
        self.console.print("[bold blue]Starting R-pentomino evolution...[/bold blue]")
        time.sleep(1)

        try:
            # 'screen=True' helps prevent flickering and handles full-terminal view
            with Live(self.generate_frame(), console=self.console, screen=True, auto_refresh=False) as live:
                while True:
                    live.update(self.generate_frame(), refresh=True)
                    self.update_grid()
                    time.sleep(self.cfg["delay_seconds"])
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Simulation stopped.[/bold yellow]")

if __name__ == "__main__":
    # You can override dimensions here if your terminal is larger
    game = RPentominoGame({"width": 120, "height": 60})
    game.setup_r_pentomino()
    game.run()