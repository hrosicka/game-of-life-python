import numpy as np
import time
from typing import Tuple, Dict, Any, Optional
from scipy.signal import convolve2d

# Import Rich for professional terminal rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class LWSSWideSimulation:
    """
    Simulates Conway's Game of Life with a wide grid optimized for LWSS movement.
    Uses SciPy for high-performance convolution and Rich for smooth terminal output.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 80,         # Wider area for longer movement
        "height": 15,        # Lower height to focus on horizontal travel
        "delay_seconds": 0.05,
        "live_cell_char": "O",
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initializes grid dimensions, configuration, and Rich console."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Initialize grid with zeros using NumPy
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_lwss_pattern(self, start_x: int, start_y: int):
        """
        Places the Lightweight Spaceship (LWSS) pattern.
        The spaceship moves from right to left in this configuration.
        """
        pattern = [
            (0, 1), (0, 4),
            (1, 0), (2, 0), (2, 4),
            (3, 0), (3, 1), (3, 2), (3, 3)
        ]
        for r, c in pattern:
            x, y = start_x + r, start_y + c
            if 0 <= x < self.height and 0 <= y < self.width:
                self.grid[x, y] = 1

    def get_grid_text(self) -> Text:
        """Generates a stylized text representation of the wide grid."""
        output = [f"[bold cyan]Wide Field Simulation: Lightweight Spaceship Movement[/bold cyan]"]
        
        # Grid border
        border = "═" * self.width
        output.append(f"[blue]╔{border}╗[/blue]")
        
        # Render each row
        for row in self.grid:
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(f"[blue]║[/blue]{line}[blue]║[/blue]")
        
        output.append(f"[blue]╚{border}╝[/blue]")
        
        # Statistics
        output.append(f"Gen: [yellow]{self.generation}[/yellow] | Field Size: {self.width}x{self.height} | Ctrl+C to stop")
        
        return Text.from_markup("\n".join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """Uses 2D convolution with boundary wrap to allow the ship to reappear."""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # 'wrap' boundary allows the spaceship to wrap around the edges
        return convolve2d(self.grid, kernel, mode='same', boundary='wrap').astype(np.int8)

    def next_generation(self):
        """Applies Game of Life rules."""
        neighbors = self._get_live_neighbor_count()
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        birth = (self.grid == 0) & (neighbors == 3)
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Main execution loop."""
        self.console.clear()
        try:
            with Live(self.get_grid_text(), console=self.console, screen=True, refresh_per_second=20) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Simulation stopped.[/bold red]")

if __name__ == "__main__":
    sim = LWSSWideSimulation()
    
    # Position adjusted: 
    # start_x (row) set to middle, 
    # start_y (column) set to far right to maximize flight path
    sim.set_lwss_pattern(start_x=5, start_y=70)
    
    sim.run()