import numpy as np
import time
import os
from typing import Tuple, Dict, Any, Optional
# Znovu zkontrolujeme import, i když by měl být v try/except bloku
from scipy.signal import convolve2d 

# Import Rich pro plynulé a profesionální vykreslování v konzoli
from rich.live import Live 
from rich.console import Console
from rich.text import Text

# Zde je kontrola instalace SciPy (přesunuto na začátek kódu)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Chyba: Pro tuto verzi je nutné mít nainstalovanou SciPy (pip install scipy).")
    exit()

class GameOfLife:
    """
    Simuluje Conwayovu Hru života pomocí SciPy pro výpočet 
    a Rich pro plynulý, živý výstup v konzoli.
    """
    # Používáme širší a vyšší rozměry pro vzor Pulsar
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 60, 
        "height": 30,
        "delay_seconds": 0.1,
        # ZMĚNA: Používáme pouze jeden znak pro každou buňku, aby se vešla na obrazovku
        "live_cell_char": "█",  # Plný blok pro lepší viditelnost
        "dead_cell_char": " "   # Jedna mezera
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Inicializuje hru s rozměry, zpožděním a nastavením konzole."""
        final_config = self.DEFAULT_CONFIG.copy()
        if config:
            final_config.update(config)
        
        self.width = final_config["width"]
        self.height = final_config["height"]
        self.delay_seconds = final_config["delay_seconds"]
        self.live_char = final_config["live_cell_char"]
        self.dead_char = final_config["dead_cell_char"]
        
        # Inicializujeme mřížku na samé mrtvé buňky
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0 
        # Inicializujeme Rich console
        self.console = Console()

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]], row_offset: int = 0, col_offset: int = 0):
        """
        Nastaví počáteční živé buňky na základě seznamu souřadnic (řádek, sloupec) 
        s možností posunu.
        """
        for r_offset, c_offset in pattern_coords:
            r, c = r_offset + row_offset, c_offset + col_offset
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    def get_grid_text(self) -> Text:
        """
        Generuje textovou reprezentaci mřížky pro Rich živé vykreslování.
        """
        # --- Zbytek této metody je stejný ---
        
        output = ["Conway's Game of Life: Pulsar"]
        
        # Okraj (nyní jen délka WIDTH + 2 pro boční okraje)
        separator = "-" * (self.width + 2) 
        output.append("+" + separator[:-2] + "+")
        
        # Obsah mřížky
        for row in self.grid:
            # Převedeme 1 na '█' a 0 na ' ' (pouze 1 znak)
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|") 
        
        # Patička a informace
        output.append("+" + separator[:-2] + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Vypočítá počet živých sousedů pro každou buňku pomocí 2D konvoluce SciPy.
        Používá 'wrap' režim hranice pro toroidní pole (cyklické hranice).
        """
        # 3x3 jádro (kromě středové buňky)
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        neighbor_counts = convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='wrap' # Toroidní hranice
        ).astype(np.int8)
        return neighbor_counts

    def next_generation(self):
        """
        Vypočítá další stav mřížky na základě Conwayových pravidel.
        """
        neighbors = self._get_live_neighbor_count()
        
        # Přežití: Živá buňka (1) A 2 nebo 3 sousedy
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Reprodukce: Mrtvá buňka (0) A přesně 3 sousedy
        reproduction_mask = (self.grid == 0) & (neighbors == 3)
        
        # Nový stav mřížky je sjednocením masek přežití a reprodukce
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Spouští hlavní simulační smyčku s plynulým Rich Live vykreslováním."""
        
        self.console.print("🚀 Spouštíme Conwayovu Hru života: Pulsar (Rich/SciPy)...")
        self.console.print("Stiskněte Ctrl+C pro zastavení.")
        time.sleep(1) 

        try:
            # Live objekt spravuje nepřetržité překreslování
            with Live(self.get_grid_text(), console=self.console) as live:
                while True:
                    # 1. Vypočítáme stav nové generace a zvýšíme počítadlo
                    self.next_generation()
                    
                    # 2. Aktualizujeme Rich Live objekt novým obsahem
                    live.update(self.get_grid_text())
                    
                    # 3. time.sleep řídí rychlost simulace
                    time.sleep(self.delay_seconds)
                    
        except KeyboardInterrupt:
            self.console.print("\nSimulace byla ukončena uživatelem.")
        except Exception as e:
            self.console.print(f"\nNastala chyba: {e}")

# --- Hlavní spouštěcí blok ---
if __name__ == "__main__":
    
    # PULSAR_PATTERN z vašeho druhého kódu, ale v seznamu pro třídu
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

    # Použijeme nastavení 60x30 a 100ms z vašeho druhého kódu
    config = {
        "width": 60,
        "height": 30,
        "delay_seconds": 1,
        # Není třeba explicitně definovat live/dead char zde, použije se DEFAULT
    }

    game = GameOfLife(config)
    
    game.set_initial_pattern(
        pattern_coords=PULSAR_PATTERN_COORDS, 
        row_offset=10, 
        col_offset=20
    )
    
    game.run_simulation()