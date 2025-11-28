import numpy as np
import time
import os
from typing import Tuple, Dict, Any, Optional
from scipy.signal import convolve2d
# Importujeme Rich pro plynulé a profesionální překreslování
from rich.live import Live 
from rich.console import Console
from rich.text import Text

# Zde předpokládáme, že SciPy je nainstalováno
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Chyba: Pro tuto verzi je nutné nainstalovat SciPy (pip install scipy).")
    exit()

class GameOfLife:
    """
    Simuluje Conway's Game of Life s využitím SciPy pro výpočet a Rich pro plynulý výstup.
    """
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 30,  
        "height": 15,
        "delay_seconds": 1.0,
        "live_cell_char": "o ",
        "dead_cell_char": "  "
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

        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        # Inicializujeme Rich konzoli
        self.console = Console()

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]]):
        for r, c in pattern_coords:
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    # Funkce _clear_screen() a print_grid() jsou nahrazeny metodou get_grid_text()
    # Tato metoda vygeneruje text, který pak Rich plynule překreslí.
    
    def get_grid_text(self) -> Text:
        """
        Generuje textovou reprezentaci mřížky pro Rich překreslování.
        """
        # --- ZACHOVÁVÁ PŮVODNÍ VIZUÁL ---
        
        # Titulek
        output = ["Conway's Game of Life"]
        
        # Ohraničení
        separator = "-" * (self.width * 2)
        output.append(separator)
        
        # Mřížka
        for row in self.grid:
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append(line)
        
        # Spodní ohraničení a info
        output.append(separator)
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        # Vracíme Rich Text objekt pro plynulý tisk
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
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
        neighbors = self._get_live_neighbor_count()
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        reproduction_mask = (self.grid == 0) & (neighbors == 3)
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Spouští simulaci s plynulým překreslováním Rich Live s manuálním sleep."""
        
        self.console.print("🚀 Starting Conway's Game of Life...")
        time.sleep(1) # Krátká pauza pro úvodní zprávu

        try:
            # ODSTRANĚN argument refresh_per_second = 1/self.delay_seconds
            with Live(self.get_grid_text(), console=self.console) as live:
                while True:
                    # 1. Spustíme novou generaci a aktualizujeme self.generation
                    self.next_generation()
                    
                    # 2. Aktualizujeme Rich Live objekt novým obsahem
                    live.update(self.get_grid_text())
                    
                    # 3. VRÁCEN time.sleep pro řízení tempa
                    time.sleep(self.delay_seconds)
                    
        except KeyboardInterrupt:
            self.console.print("\nSimulation terminated by user.")
        except Exception as e:
            self.console.print(f"\nAn error occurred: {e}")

# --- Hlavní spouštěcí blok ---
if __name__ == "__main__":
    
    game = GameOfLife()
    
    # Inicializace - TOAD oscillátory
    initial_pattern = [
        (5, 10), (5, 11), (5, 12),
        (6, 9), (6, 10), (6, 11),
        (10, 12), (10, 13), (10, 14),
        (11, 11), (11, 12), (11, 13)
    ]
    
    game.set_initial_pattern(initial_pattern)
    
    # Původní titulek se ukáže hned, než Live převezme kontrolu
    game.console.print("🚀 Starting Conway's Game of Life...")
    time.sleep(1) 
    
    game.run_simulation()