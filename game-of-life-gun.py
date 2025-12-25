import numpy as np
import time
from typing import Tuple, Dict, Any, Optional, List
from scipy.signal import convolve2d

# Import Rich pro hladké a profesionální vykreslování v konzoli
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLifeGun:
    """
    Simulace Conwayovy Hry života se zaměřením na Gosper Glider Gun.
    Využívá SciPy pro matematické výpočty a Rich pro live rendering.
    """
    
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 100,
        "height": 40,
        "delay_seconds": 0.01,  # Rychlejší pro plynulý pohyb gliderů
        "live_cell_char": "X",
        "dead_cell_char": " "
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Inicializace mřížky, konfigurace a konzole."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]

        # Inicializace mřížky pomocí NumPy (všude nuly)
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        self.console = Console()

    def set_gosper_glider_gun(self, start_x: int, start_y: int):
        """Definuje a umístí vzor Gosper Glider Gun do mřížky."""
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
        """Sestaví vizuální reprezentaci mřížky pro Rich."""
        output = [f"[bold green]Conway's Game of Life - Gosper Glider Gun[/bold green]"]
        
        # Horní ohraničení
        separator = "─" * self.width
        output.append(f"[blue]{separator}[/blue]")
        
        # Obsah mřížky
        for row in self.grid:
            # Vytvoření řádku: X pro živé, mezera pro mrtvé
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(line)
        
        # Patička
        output.append(f"[blue]{separator}[/blue]")
        output.append(f"Gen: [yellow]{self.generation}[/yellow] | Speed: {1/self.delay_seconds:.1f} fps | Ctrl+C pro stop")
        
        return Text.from_markup("\n".join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """Vypočítá počet sousedů pomocí 2D konvoluce (rychlejší než cykly)."""
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # mode='same' zachová rozměry, boundary='fill' simuluje okraje z C kódu
        return convolve2d(self.grid, kernel, mode='same', boundary='fill', fillvalue=0)

    def next_generation(self):
        """Aplikuje pravidla Game of Life na celou matici najednou."""
        neighbors = self._get_live_neighbor_count()
        
        # Pravidlo 1 & 2: Přežití (buňka žije a má 2 nebo 3 sousedy)
        survival = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Pravidlo 3: Reprodukce (buňka je mrtvá a má přesně 3 sousedy)
        birth = (self.grid == 0) & (neighbors == 3)
        
        self.grid = (survival | birth).astype(np.int8)
        self.generation += 1

    def run(self):
        """Hlavní smyčka simulace s plynulým překreslováním."""
        self.console.clear()
        self.console.print("[bold cyan]Iniciuji Gosper Glider Gun...[/bold cyan]")
        time.sleep(1)

        try:
            with Live(self.get_grid_text(), console=self.console, screen=True, refresh_per_second=60) as live:
                while True:
                    self.next_generation()
                    live.update(self.get_grid_text())
                    time.sleep(self.delay_seconds)
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Simulace ukončena.[/bold red]")

if __name__ == "__main__":
    # Vytvoření instance s vlastním nastavením
    sim = GameOfLifeGun()
    
    # Umístění Gun patternu (odsazení 5, 5 jako v původním C kódu)
    sim.set_gosper_glider_gun(5, 5)
    
    # Spuštění
    sim.run()