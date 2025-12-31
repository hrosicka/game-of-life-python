import numpy as np
import time
from typing import Tuple, Dict, Any, Optional, List

# Check for SciPy installation for fast 2D convolution
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed (pip install scipy).")
    exit()

# Import Rich for professional terminal rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLifePulsar:
    """
    Simulates Conway's Game of Life focusing on the Pulsar oscillator.
    Uses SciPy for computation and Rich for smooth console output.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 60,
        "height": 30,
        "delay_seconds": 0.1,  # Standard pace for Pulsar oscillation
        "live_cell_char": "█",  # Full block for high visibility
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the grid, configuration, and console."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize grid with zeros (all dead)
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_pulsar_pattern(self, row_offset: int, col_offset: int):
        """
        Defines and places the Pulsar pattern (Period 3 oscillator).
        Coordinates are relative to the offset.
        """
        pattern_coords = [
            (1, 3), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11),
            (3, 1), (3, 6), (3, 8), (3, 13),
            (4, 1), (4, 6), (4, 8), (4, 13),
            (5, 1), (5, 6), (5, 8), (5, 13),
            (6, 3), (6, 4), (6, 5), (6, 9), (6, 10), (6, 11),
            (8, 3), (8, 4), (8, 5), (8, 9), (8, 10), (8, 11),
            (9, 1), (9, 6), (9, 8), (9, 13),
            (10, 1), (10, 6), (10, 8), (10, 13),
            (11, 1), (11, 6), (11, 8), (11, 13),
            (13, 3), (13, 4), (13, 5), (13, 9), (13, 10), (13, 11),
        ]
        
        for r, c in pattern_coords:
            target_r, target_c = r + row_offset, c + col_offset
            if 0 <= target_r < self.height and 0 <= target_c < self.width:
                self.grid[target_r, target_c] = 1

    def get_grid_text(self) -> Text:
        """Generates the visual frame for Rich rendering."""
        output = ["Conway's Game of Life: Pulsar (Period 3 Oscillator)"]
        
        # Consistent border design
        separator = "-" * self.width
        output.append("+" + separator + "+")
        
        # Build grid content
        for row in self.grid:
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|")
        
        output.append("+" + separator + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Gen: {self.generation} | Ctrl+C to stop")
        
        return Text('\n'.join(output), style="bold magenta")

    def _get_live_neighbor_count(self) -> np.ndarray:
        """Calculates neighbors using 2D convolution with toroidal (wrap) boundaries."""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        return convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='wrap' # Cyclic field
        ).astype(np.int8)

    def next_generation(self):
        """Updates the grid state based on standard rules."""
        neighbors = self._get_live_neighbor_count()
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Starts the main simulation loop."""
        self.console.clear()
        try:
            with Live(self.get_grid_text(), console=self.console, screen=True) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Simulation stopped by user.[/bold yellow]")

if __name__ == "__main__":
    # Pulsar fits perfectly in a 60x30 grid
    config = {
        "width": 60,
        "height": 30,
        "delay_seconds": 0.1, 
    }

    sim = GameOfLifePulsar(config)
    
    # Place Pulsar roughly in the center
    sim.set_pulsar_pattern(row_offset=7, col_offset=23)
    
    sim.run()