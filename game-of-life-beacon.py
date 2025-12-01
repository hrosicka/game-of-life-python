import numpy as np
import time
from typing import Tuple, Dict, Any, Optional

# Import SciPy for fast neighbor counting (Convolution)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed for this version (pip install scipy).")
    exit()

# Import Rich for smooth, live console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLife:
    """
    Simulates Conway's Game of Life using SciPy for computation 
    and Rich for smooth, live console output.
    """
    # Configuration for the Beacon pattern (smaller grid, longer delay for oscillation)
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 30,    
        "height": 10,
        "delay_seconds": 1.0, # 1.0s for good visibility of period-2 oscillation
        "live_cell_char": "O", # Using a single character, as in your C code
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the game with dimensions, delay, and console settings."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize the grid (dead cells = 0)
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        # Initialize the Rich console
        self.console = Console()

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]], row_offset: int = 0, col_offset: int = 0):
        """
        Sets the initial live cells based on a list of coordinates (row, column) 
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
        output = ["Conway's Game of Life: Beacon Oscillator (Period 2)"]
        
        # Border (width + 2 for side borders)
        separator = "-" * (self.width + 2) 
        output.append("+" + separator[:-2] + "+")
        
        # Grid content
        for row in self.grid:
            # Convert 1 to 'O' and 0 to ' ' (one character per cell)
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|")
        
        # Footer and information
        output.append("+" + separator[:-2] + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        # Return a Rich Text object for smooth rendering
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Calculates the number of live neighbors for each cell using SciPy's 2D convolution.
        Your C code did not use toroidal boundaries, so we use the 'fill' mode
        with zeros for the edges ('same' mode with 'fill' boundary).
        """
        # 3x3 kernel (excluding the center cell)
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # Using 'fill' with zero padding matches the logic of your C code
        # (where neighbors outside the boundaries are ignored, which is equivalent to zero).
        neighbor_counts = convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='fill', # Non-wraparound mode, like in your C code
            fillvalue=0
        ).astype(np.int8)
        return neighbor_counts

    def next_generation(self):
        """
        Calculates the next state of the grid based on Conway's rules.
        """
        neighbors = self._get_live_neighbor_count()
        
        # 1. & 2. & 3. Survival: A live cell (1) AND 2 or 3 neighbors
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # 4. Reproduction: A dead cell (0) AND exactly 3 neighbors
        reproduction_mask = (self.grid == 0) & (neighbors == 3)
        
        # The new grid state is the union of the survival and reproduction masks
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Starts the main simulation loop with smooth Rich Live rendering."""
        
        self.console.print("🚀 Starting Conway's Game of Life: Beacon (Rich/SciPy)...")
        self.console.print("Press Ctrl+C to stop.")
        time.sleep(1) 

        try:
            # The Live object manages continuous redrawing
            with Live(self.get_grid_text(), console=self.console) as live:
                while True:
                    # 1. Calculate the new generation state and increment the counter
                    self.next_generation()
                    
                    # 2. Update the Rich Live object with the new content
                    live.update(self.get_grid_text())
                    
                    # 3. time.sleep controls the simulation speed
                    time.sleep(self.delay_seconds)
                    
        except KeyboardInterrupt:
            self.console.print("\nSimulation terminated by user.")
        except Exception as e:
            self.console.print(f"\nAn error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    
    # Beacon Pattern: (row, column) offsets
    BEACON_PATTERN_COORDS = [
        (0, 0), (0, 1), 
        (1, 0), (1, 1), # Top-left block
        (2, 2), (2, 3), 
        (3, 2), (3, 3)  # Bottom-right block
    ]
    
    # Use C code settings, but with a 0.2s delay for oscillation visibility
    config = {
        "width": 30,
        "height": 10,
        "delay_seconds": 0.2,
    }

    game = GameOfLife(config)
    
    # Placing the pattern in the center of the grid, similar to (3, 3) in a small C code
    game.set_initial_pattern(
        pattern_coords=BEACON_PATTERN_COORDS, 
        row_offset=3, 
        col_offset=12
    )
    
    game.run_simulation()