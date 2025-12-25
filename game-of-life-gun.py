import numpy as np
import time
from typing import Tuple, Dict, Any, Optional, List
from scipy.signal import convolve2d

# Import Rich for smooth and professional console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLifeGun:
    """
    Simulates Conway's Game of Life focusing on the Gosper Glider Gun.
    Uses SciPy for mathematical calculations and Rich for live console rendering.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 100,
        "height": 40,
        "delay_seconds": 0.01,  # Lower delay for smooth glider movement
        "live_cell_char": "X",
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes grid, configuration, and console setup."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize grid using NumPy (all zeros)
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_gosper_glider_gun(self, start_x: int, start_y: int):
        """
        Defines and places the Gosper Glider Gun pattern into the grid.
        Coordinates are relative to the start_x and start_y position.
        """
        pattern = [
            (1, 25), (2, 23), (2, 25),
            (3, 13), (3, 14), (3, 21), (3, 22), (3, 35), (3, 36),
            (4, 12), (4, 16), (4, 21), (4, 22), (4, 35), (4, 36),
            (5, 1), (5, 2), (5, 11), (5, 17), (5, 21), (5, 22),
            (6, 1), (6, 2), (6, 11), (6, 15), (6, 17), (6, 18), (6, 23), (6, 25),
            (7, 11), (7, 17), (7, 25),
            (8, 12), (8, 16),
            (9, 13), (9, 14)
        ]
        for r, c in pattern:
            x, y = start_x + r, start_y + c
            if 0 <= x < self.height and 0 <= y < self.width:
                self.grid[x, y] = 1

    def get_grid_text(self) -> Text:
        """Generates the visual representation of the grid for Rich rendering."""
        output = [f"[bold green]Conway's Game of Life - Gosper Glider Gun[/bold green]"]
        
        # Top border
        separator = "─" * self.width
        output.append(f"[blue]{separator}[/blue]")
        
        # Grid content
        for row in self.grid:
            # Create row string: 'X' for live, space for dead
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(line)
        
        # Footer
        output.append(f"[blue]{separator}[/blue]")
        output.append(f"Gen: [yellow]{self.generation}[/yellow] | Speed: {1/self.delay_seconds:.1f} fps | Ctrl+C to stop")
        
        return Text.from_markup("\n".join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Calculates neighbor counts using 2D convolution.
        This is significantly faster than nested loops in Python.
        """
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # mode='same' keeps dimensions, boundary='fill' mimics the C code boundary logic
        return convolve2d(self.grid, kernel, mode='same', boundary='fill', fillvalue=0)

    def next_generation(self):
        """Applies Conway's Game of Life rules to the entire matrix at once."""
        neighbors = self._get_live_neighbor_count()
        
        # Rule 1 & 2: Survival (cell is alive and has 2 or 3 neighbors)
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Rule 3: Reproduction (cell is dead and has exactly 3 neighbors)
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Main simulation loop with smooth live updating."""
        self.console.clear()
        self.console.print("[bold cyan]Initializing Gosper Glider Gun...[/bold cyan]")
        time.sleep(1)

        try:
            # screen=True enables an alternate buffer (similar to full-screen apps)
            with Live(self.get_grid_text(), console=self.console, screen=True, refresh_per_second=60) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Simulation stopped by user.[/bold red]")

if __name__ == "__main__":
    # Create an instance with default configuration
    sim = GameOfLifeGun()
    
    # Place the Gun pattern (offset 5, 5 matching the original C code)
    sim.set_gosper_glider_gun(5, 5)
    
    # Start the simulation
    sim.run()