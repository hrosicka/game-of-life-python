import numpy as np
import time
from typing import Tuple, Dict, Any, Optional

# Import SciPy for fast neighbor counting (Convolution)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Chyba: SciPy musí být nainstalována pro tuto verzi (pip install scipy).")
    exit()

# Import Rich for smooth, live console rendering
from rich.live import Live 
from rich.console import Console
from rich.text import Text

class GameOfLife:
    """
    Simuluje Conwayovu Hru života pomocí SciPy pro výpočet 
    a Rich pro plynulý, živý výstup v konzoli.
    """
    # Nastavení pro vzor Beacon (menší mřížka, delší delay pro oscilaci)
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 30,    
        "height": 10,
        "delay_seconds": 1.0, # 1.0s pro dobrou viditelnost period-2 oscilace
        "live_cell_char": "O", # Používáme jeden znak jako ve vašem C kódu
        "dead_cell_char": " "
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

        # Inicializujeme mřížku (mrtvé buňky = 0)
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
        output = ["Conway's Game of Life: Beacon Oscillator (Period 2)"]
        
        # Okraj (šířka + 2 pro boční okraje)
        separator = "-" * (self.width + 2) 
        output.append("+" + separator[:-2] + "+")
        
        # Obsah mřížky
        for row in self.grid:
            # Převedeme 1 na 'O' a 0 na ' ' (jeden znak na buňku)
            line = "".join([self.live_char if cell == 1 else self.dead_char for cell in row])
            output.append("|" + line + "|")
        
        # Patička a informace
        output.append("+" + separator[:-2] + "+")
        output.append(f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}")
        
        # Vrátíme Rich Text objekt pro plynulé vykreslování
        return Text('\n'.join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Vypočítá počet živých sousedů pro každou buňku pomocí 2D konvoluce SciPy.
        Váš C kód nepoužíval toroidní hranice, takže použijeme 'fill' režim
        s nulami pro okraje ('same' mode with 'fill' boundary).
        """
        # 3x3 jádro (kromě středové buňky)
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.int8)
        
        # Použití 'fill' s paddingem nul odpovídá logice vašeho C kódu
        # (kde se sousedi mimo hranice ignorují, což je ekvivalentní nule).
        neighbor_counts = convolve2d(
            self.grid, 
            kernel, 
            mode='same', 
            boundary='fill', # Nekruhový režim, jako ve vašem C kódu
            fillvalue=0
        ).astype(np.int8)
        return neighbor_counts

    def next_generation(self):
        """
        Vypočítá další stav mřížky na základě Conwayových pravidel.
        """
        neighbors = self._get_live_neighbor_count()
        
        # 1. & 2. & 3. Přežití: Živá buňka (1) A 2 nebo 3 sousedy
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # 4. Reprodukce: Mrtvá buňka (0) A přesně 3 sousedy
        reproduction_mask = (self.grid == 0) & (neighbors == 3)
        
        # Nový stav mřížky je sjednocením masek přežití a reprodukce
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Spouští hlavní simulační smyčku s plynulým Rich Live vykreslováním."""
        
        self.console.print("🚀 Spouštíme Conwayovu Hru života: Beacon (Rich/SciPy)...")
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
    
    # Beacon Pattern: (row, column) offsets
    BEACON_PATTERN_COORDS = [
        (0, 0), (0, 1), 
        (1, 0), (1, 1), # Horní levý blok
        (2, 2), (2, 3), 
        (3, 2), (3, 3)  # Dolní pravý blok
    ]
    
    # Použijeme nastavení z C kódu, ale s delay 1.0s pro viditelnost oscilace
    config = {
        "width": 30,
        "height": 10,
        "delay_seconds": 0.2,
    }

    game = GameOfLife(config)
    
    # Umístění vzoru do středu mřížky, podobně jako (3, 3) v malém C kódu
    game.set_initial_pattern(
        pattern_coords=BEACON_PATTERN_COORDS, 
        row_offset=3, 
        col_offset=12
    )
    
    game.run_simulation()