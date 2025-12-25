import numpy as np
import time
from typing import Dict, Any, Optional
from scipy.signal import convolve2d

from rich.live import Live 
from rich.console import Console
from rich.text import Text

class LWSSAgingSimulation:
    """
    Conway's Game of Life with aging cells.
    New cells are white, older cells transition through cyan to deep blue.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 80,
        "height": 15,
        "delay_seconds": 0.05,
        "live_cell_char": "O",
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Grid stores integers (0 = dead, 1+ = age in generations)
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)
        self.generation = 0 
        self.console = Console()

    def set_lwss_pattern(self, start_x: int, start_y: int):
        pattern = [(0, 1), (0, 4), (1, 0), (2, 0), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3)]
        for r, c in pattern:
            x, y = start_x + r, start_y + c
            if 0 <= x < self.height and 0 <= y < self.width:
                self.grid[x, y] = 1

    def get_color_for_age(self, age: int) -> str:
        """Returns a Rich color tag based on the age of the cell."""
        if age <= 1: return "bold white"
        if age == 2: return "bright_cyan"
        if age == 3: return "cyan"
        if age == 4: return "turquoise2"
        if age <= 7: return "dodger_blue1"
        return "blue3" # Oldest cells

    def get_grid_text(self) -> Text:
        """Generates a stylized text representation with aging colors."""
        text = Text()
        text.append(f"Game of Life: Aging LWSS | Gen: {self.generation}\n", style="bold magenta")
        
        border_style = "blue"
        text.append(f"╔{'═' * self.width}╗\n", style=border_style)
        
        for row in self.grid:
            text.append("║", style=border_style)
            for cell_age in row:
                if cell_age > 0:
                    color = self.get_color_for_age(cell_age)
                    text.append(self.live_char, style=color)
                else:
                    text.append(self.dead_char)
            text.append("║\n", style=border_style)
        
        text.append(f"╚{'═' * self.width}╝", style=border_style)
        return text

    def next_generation(self):
        """Calculates next generation and increments age of surviving cells."""
        # Create a binary mask for convolution
        binary_grid = (self.grid > 0).astype(np.int8)
        
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)
        neighbors = convolve2d(binary_grid, kernel, mode='same', boundary='wrap')

        # Apply rules
        survives = (binary_grid == 1) & ((neighbors == 2) | (neighbors == 3))
        born = (binary_grid == 0) & (neighbors == 3)

        # New grid logic
        new_grid = np.zeros_like(self.grid)
        # Surviving cells: increment their current age
        new_grid[survives] = self.grid[survives] + 1
        # Newborn cells: age starts at 1
        new_grid[born] = 1

        self.grid = new_grid
        self.generation += 1

    def run(self):
        self.console.clear()
        try:
            with Live(self.get_grid_text(), console=self.console, screen=True, auto_refresh=False) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text(), refresh=True)
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Simulation stopped.[/bold red]")

if __name__ == "__main__":
    sim = LWSSAgingSimulation()
    sim.set_lwss_pattern(5, 70)
    sim.run()