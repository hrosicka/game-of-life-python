import numpy as np
import time
import os
from typing import Tuple, Dict, Any, Optional
from scipy.signal import convolve2d
# Import Rich for smooth and professional console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

# Check for SciPy installation
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed for this version (pip install scipy).")
    exit()

class GameOfLife:
    """
    Simulates Conway's Game of Life using SciPy for calculation 
    and Rich for smooth, live console output.
    """
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 30,  
        "height": 15,
        "delay_seconds": 1.0,
        "live_cell_char": "o ",
        "dead_cell_char": "  "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the game with dimensions, delay, and console setup."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize grid to all dead cells
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        # Initialize Rich console
        self.console = Console()

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]]):
        """Sets the initial live cells based on a list of (row, column) coordinates."""
        for r, c in pattern_coords:
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    # The _clear_screen() and print_grid() functions are replaced by the get_grid_text() method.
    # This method generates the text output, which Rich then smoothly redraws.
    
    def get_grid_text(self) -> Text:
        """
        Generates the text representation of the grid for Rich live rendering, 
        preserving the original visual style.
        """
        # --- PRESERVES ORIGINAL VISUAL STYLE ---
        
        output = ["Conway's Game of Life"]
        
        # Border
        separator = "-" * (self.width * 2)
        output.append(separator)
        
        # Grid content
        for row in self.grid:
            # Convert 1 to 'o ' and 0 to '  '
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(line)
        
        # Footer and info
        output.append(separator)
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        # Return a Rich Text object for smooth printing
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Calculates the live neighbor count for every cell using SciPy's 2D convolution.
        Uses 'wrap' boundary mode for a toroidal field.
        """
        # 3x3 kernel (excluding the center cell)
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        neighbor_counts = convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='wrap'
        ).astype(np.int8)
        return neighbor_counts

    def next_generation(self):
        """
        Calculates the next state of the grid based on Conway's rules.
        """
        neighbors = self._get_live_neighbor_count()
        
        # Survival: Live cell (1) AND 2 or 3 neighbors
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Reproduction: Dead cell (0) AND exactly 3 neighbors
        reproduction_mask = (self.grid == 0) & (neighbors == 3)
        
        # The new grid state is the union of survival and reproduction masks
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Runs the main simulation loop with smooth Rich Live rendering."""
        
        self.console.print("🚀 Starting Conway's Game of Life...")
        time.sleep(1) # Short pause for the initial message

        try:
            # Live object manages the continuous redrawing
            with Live(self.get_grid_text(), console=self.console) as live:
                while True:
                    # 1. Calculate the new generation state and increment count
                    self.next_generation()
                    
                    # 2. Update the Rich Live object with the new content
                    live.update(self.get_grid_text())
                    
                    # 3. Use time.sleep to control the simulation pace (delay_seconds)
                    time.sleep(self.delay_seconds)
                    
        except KeyboardInterrupt:
            self.console.print("\nSimulation terminated by user.")
        except Exception as e:
            self.console.print(f"\nAn error occurred: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    
    game = GameOfLife()
    
    # Initialization - TOAD oscillators pattern
    initial_pattern = [
        (5, 10), (5, 11), (5, 12),
        (6, 9), (6, 10), (6, 11),
        (10, 12), (10, 13), (10, 14),
        (11, 11), (11, 12), (11, 13)
    ]
    
    game.set_initial_pattern(initial_pattern)
    
    # Run the simulation (The initial print is outside the loop to prevent repetition)
    game.run_simulation()