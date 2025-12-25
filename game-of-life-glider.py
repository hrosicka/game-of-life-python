import numpy as np
import time
from typing import Tuple, Dict, Any, Optional
from scipy.signal import convolve2d

# Import Rich for professional console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GliderSimulation:
    """
    Simulates Conway's Game of Life with toroidal (wrap-around) boundaries.
    Uses SciPy for convolution and Rich for high-performance rendering.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 30,
        "height": 15,
        "delay_seconds": 0.5,
        "live_cell_char": "o ",
        "dead_cell_char": ". "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes the simulation environment and NumPy grid."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize grid with zeros
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_initial_patterns(self):
        """Sets the initial GLIDER1 and GLIDER2 patterns as defined in the C code."""
        # GLIDER1 coordinates
        glider1 = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        
        # GLIDER2 coordinates
        glider2 = [(5, 5), (6, 6), (7, 4), (7, 5), (7, 6)]

        for r, c in glider1 + glider2:
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    def get_grid_text(self) -> Text:
        """Generates the Rich-formatted text for the current grid state."""
        output = [f"[bold cyan]Conway's Game of Life - Glider Patterns[/bold cyan]"]
        
        # Grid content rendering
        for row in self.grid:
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(line)
        
        # Metadata footer
        output.append(f"[dim]Generation: {self.generation} | Toroidal: Yes | Delay: {self.delay_seconds}s[/dim]")
        output.append("[italic grey37]Press Ctrl+C to exit[/italic grey37]")
        
        return Text.from_markup("\n".join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Calculates neighbors using convolution with 'wrap' boundary mode.
        This handles the wrap-around edges automatically.
        """
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # 'wrap' boundary is equivalent to the modulo arithmetic in your C code
        return convolve2d(self.grid, kernel, mode='same', boundary='wrap').astype(np.int8)

    def next_generation(self):
        """Updates the grid based on standard Life rules."""
        neighbors = self._get_live_neighbor_count()
        
        # Logic: (Alive and 2-3 neighbors) OR (Dead and 3 neighbors)
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        reproduction = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | reproduction).astype(np.int8)
        self.generation += 1

    def run(self):
        """Executes the simulation loop."""
        self.console.clear()
        try:
            with Live(self.get_grid_text(), console=self.console, screen=True) as live:
                while True:
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
                    self.next_generation()
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Simulation terminated.[/bold yellow]")

if __name__ == "__main__":
    # Setup and run
    sim = GliderSimulation()
    sim.set_initial_patterns()
    sim.run()