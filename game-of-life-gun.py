import numpy as np
import time
from typing import Tuple, Dict, Any, Optional, List

# Import SciPy for fast neighbor counting (Convolution)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed (pip install scipy).")
    exit()

# Import Rich for professional live console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLifeGun:
    """
    Simulates Conway's Game of Life with a focus on the Gosper Glider Gun.
    The design is optimized for terminal clarity with a classic ASCII border.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 80,
        "height": 40,
        "delay_seconds": 0.05,
        "live_cell_char": "O",
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the simulation environment and terminal settings."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize the grid as a NumPy matrix
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_gosper_glider_gun(self, row_offset: int, col_offset: int):
        """
        Populates the grid with the Gosper Glider Gun, the first known 
        stationary pattern that emits gliders forever.
        """
        # Gosper Glider Gun relative coordinates
        pattern = [
            (5, 1), (5, 2), (6, 1), (6, 2),                  # Left block
            (5, 11), (6, 11), (7, 11), (4, 12), (8, 12),      # Left circle
            (3, 13), (9, 13), (3, 14), (9, 14), (6, 15),
            (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18),
            (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), # Middle machinery
            (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25),
            (3, 35), (4, 35), (3, 36), (4, 36)               # Right block
        ]
        
        for r, c in pattern:
            target_r, target_c = r + row_offset, c + col_offset
            if 0 <= target_r < self.height and 0 <= target_c < self.width:
                self.grid[target_r, target_c] = 1

    def get_grid_text(self) -> Text:
        """
        Generates the visual frame including the title, borders, and grid state.
        Matches the requested legacy terminal design.
        """
        output = ["Conway's Game of Life: Gosper Glider Gun (Infinite Emission)"]
        
        # Border construction
        separator = "-" * (self.width) 
        output.append("+" + separator + "+")
        
        # Matrix to String conversion
        for row in self.grid:
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|")
        
        output.append("+" + separator + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation} | Press Ctrl+C to exit")
        
        return Text('\n'.join(output), style="bold green")

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Uses 2D convolution to count neighbors for every cell simultaneously.
        Matches standard boundary conditions (dead cells beyond borders).
        """
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        return convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='fill', 
            fillvalue=0
        ).astype(np.int8)

    def next_generation(self):
        """Updates the grid based on Conway's core B3/S23 rules."""
        neighbors = self._get_live_neighbor_count()
        
        # Apply logic: Survival and Birth
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Starts the simulation loop with live rendering."""
        self.console.clear()
        self.console.print("[cyan]Readying the Gosper Glider Gun...[/cyan]")
        time.sleep(1) 

        try:
            with Live(self.get_grid_text(), console=self.console, screen=True) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Simulation terminated.[/yellow]")

if __name__ == "__main__":
    # Optimal dimensions for the Gun to fire several gliders
    config = {
        "width": 80,
        "height": 24,
        "delay_seconds": 0.02,
    }

    game = GameOfLifeGun(config)
    
    # Position the Gun in the top-left area so gliders have space to travel
    game.set_gosper_glider_gun(row_offset=2, col_offset=2)
    
    game.run_simulation()