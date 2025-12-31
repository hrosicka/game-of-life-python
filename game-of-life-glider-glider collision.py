import numpy as np
import time
from typing import Tuple, Dict, Any, Optional, List

# Check for SciPy dependency at startup
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed (pip install scipy).")
    exit()

from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GliderCollisionGame:
    """
    Simulates a head-on collision between two gliders using NumPy and SciPy.
    """
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 50,    
        "height": 25,
        "delay_seconds": 0.08,
        "live_char": "O",
        "dead_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the grid and configuration."""
        cfg = {**self.DEFAULT_CONFIG, **(config or {})}
        self.width, self.height = cfg["width"], cfg["height"]
        self.delay = cfg["delay_seconds"]
        self.live_char = cfg["live_char"]
        self.dead_char = cfg["dead_char"]

        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def add_pattern(self, pattern: List[Tuple[int, int]], r_off: int, c_off: int, flip_h: bool = False, flip_v: bool = False):
        """
        Adds a pattern to the grid with optional flipping.
        Useful for changing glider directions.
        """
        for r, c in pattern:
            curr_r = (r_off - r) if flip_v else (r_off + r)
            curr_c = (c_off - c) if flip_h else (c_off + c)
            
            if 0 <= curr_r < self.height and 0 <= curr_c < self.width:
                self.grid[curr_r, curr_c] = 1

    def render(self) -> Text:
        """Generates the Rich-formatted text for terminal display."""
        header = f"Glider Mid-Air Collision | Gen: {self.generation}\n"
        border = "+" + "-" * self.width + "+"
        
        # Fast vectorized conversion of grid to characters
        chars = np.where(self.grid == 1, self.live_char, self.dead_char)
        body = "\n".join(["|" + "".join(row) + "|" for row in chars])
        
        return Text(header + border + "\n" + body + "\n" + border, style="bold cyan")

    def step(self):
        """Computes the next generation using 2D convolution."""
        # Standard Moore neighborhood kernel
        kernel = np.array([[1,1,1],
                           [1,0,1],
                           [1,1,1]], dtype=np.int8)
        
        neighbors = convolve2d(self.grid, kernel, mode='same', boundary='fill')
        
        # Apply B3/S23 rules
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Starts the main simulation loop with live rendering."""
        self.console.clear()
        try:
            with Live(self.render(), console=self.console, screen=True) as live:
                while True:
                    live.update(self.render())
                    self.step()
                    time.sleep(self.delay)
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Simulation stopped by user.[/bold yellow]")

if __name__ == "__main__":
    # Standard Glider relative coordinates
    GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    
    # Use a larger grid for better visibility of the approach
    game = GliderCollisionGame({"width": 60, "height": 30, "delay_seconds": 0.1})
    
    # GLIDER 1: Top-left corner, moving South-East
    game.add_pattern(GLIDER, r_off=2, c_off=2)
    
    # GLIDER 2: Bottom-right area, moving North-West
    # Coordinates r_off=22, c_off=22 put it on a direct collision path
    game.add_pattern(GLIDER, r_off=22, c_off=22, flip_h=True, flip_v=True)
    
    game.run()