import numpy as np
import time
import os
from typing import Tuple, Dict, Any, Optional
# Re-check the import, although it should be caught in the try/except block
from scipy.signal import convolve2d 

# Import Rich for smooth and professional console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

# Check for SciPy installation (moved to the start of the code)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed for this version (pip install scipy).")
    exit()

class GameOfLife:
    """
    Simulates Conway's Game of Life using SciPy for fast calculation 
    and Rich for smooth, live console output.
    """
    # Using wider and taller dimensions for the Pulsar pattern
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 60, 
        "height": 30,
        "delay_seconds": 0.1,
        # CHANGE: Using only one character per cell so it fits the screen
        "live_cell_char": "█",  # Full block for better visibility
        "dead_cell_char": " "   # A single space
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the game with dimensions, delay, and console setup."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        # Note: delay_seconds was set to 1 in your config, but 0.1 is standard for Pulsar.
        # I'll use the 1.0 from your latest request, as it was passed in the config.
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

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]], row_offset: int = 0, col_offset: int = 0):
        """
        Sets the initial live cells based on a list of (row, column) coordinates 
        with an optional offset.
        """
        for r_offset, c_offset in pattern_coords:
            r, c = r_offset + row_offset, c_offset + col_offset
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    def get_grid_text(self) -> Text:
        """
        Generates the text representation of the grid for Rich live rendering.
        """
        # --- The rest of this method is the same logic ---
        
        output = ["Conway's Game of Life: Pulsar"]
        
        # Border (now only the length of WIDTH + 2 for side borders)
        separator = "-" * (self.width + 2) 
        output.append("+" + separator[:-2] + "+")
        
        # Grid content
        for row in self.grid:
            # Convert 1 to '█' and 0 to ' ' (only 1 character)
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|") 
        
        # Footer and info
        output.append("+" + separator[:-2] + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Calculates the live neighbor count for every cell using SciPy's 2D convolution.
        Uses 'wrap' boundary mode for a toroidal field (cyclic boundaries).
        """
        # 3x3 kernel (excluding the center cell)
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        neighbor_counts = convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='wrap' # Toroidal boundaries
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
        
        self.console.print("🚀 Starting Conway's Game of Life: Pulsar (Rich/SciPy)...")
        self.console.print("Press Ctrl+C to stop.")
        time.sleep(1) 

        try:
            # Live object manages the continuous redrawing
            with Live(self.get_grid_text(), console=self.console) as live:
                while True:
                    # 1. Calculate the new generation state and increment count
                    self.next_generation()
                    
                    # 2. Update the Rich Live object with the new content
                    live.update(self.get_grid_text())
                    
                    # 3. time.sleep controls the simulation pace
                    time.sleep(self.delay_seconds)
                    
        except KeyboardInterrupt:
            self.console.print("\nSimulation terminated by user.")
        except Exception as e:
            self.console.print(f"\nAn error occurred: {e}")

# --- Main Execution Block ---
if __name__ == "__main__":
    
    # PULSAR_PATTERN from your second code, now as a list of coordinates
    PULSAR_PATTERN_COORDS = [
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

    # Use the 60x30 and 1.0s settings from your last request
    config = {
        "width": 60,
        "height": 30,
        "delay_seconds": 1.0, 
    }

    game = GameOfLife(config)
    
    # Place the Pulsar pattern in the grid with offsets
    game.set_initial_pattern(
        pattern_coords=PULSAR_PATTERN_COORDS, 
        row_offset=10, 
        col_offset=20
    )
    
    game.run_simulation()