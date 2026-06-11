import numpy as np
import time
from typing import Dict, Any, Optional, Tuple
from scipy.signal import convolve2d

# Import Rich for smooth and professional console rendering
# Pokud ještě nemáš, instaluj: pip install rich
from rich.live import Live
from rich.console import Console
from rich.text import Text

# Zkontrolovat instalaci SciPy (stejně jako v tvém původním Python kódu)
try:
    from scipy.signal import convolve2d
except ImportError:
    print("Error: SciPy must be installed for this version (pip install scipy).")
    exit()


class GameOfLife:
    """
    Simuluje Conway's Game of Life pomocí SciPy pro výpočet
    a Rich pro plynulý, živý výstup do konzole.
    """

    # Nastavení odpovídající C kódu: WIDTH 15, HEIGHT 7, Delay 0.5s (500 ms)
    DEFAULT_CONFIG: Dict[str, Any] = {
        "width": 15,
        "height": 7,
        "delay_seconds": 0.5,  # C kód používal Sleep(500) pro 500 ms, tj. 0.5 sekundy
        "live_cell_char": "o ",
        "dead_cell_char": "  ",
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

        # Inicializace mřížky na všechny mrtvé buňky
        self.grid = np.zeros((self.height, self.width), dtype=np.int8)
        self.generation = 0
        # Inicializace Rich konzole
        self.console = Console()

    def set_initial_pattern(self, pattern_coords: list[Tuple[int, int]]):
        """Nastaví počáteční živé buňky na základě seznamu souřadnic (řádek, sloupec)."""
        for r, c in pattern_coords:
            if 0 <= r < self.height and 0 <= c < self.width:
                self.grid[r, c] = 1

    def get_grid_text(self) -> Text:
        """
        Generuje textovou reprezentaci mřížky pro Rich live rendering.
        """
        output = ["Conway's Game of Life - Blinker"]

        # Odsazení pro lepší vzhled a zarovnání
        padding = " " * 4

        # Horní ohraničení (volitelné, ale pěkné)
        separator = "-" * (self.width * 2)
        output.append(padding + separator)

        # Obsah mřížky
        for row in self.grid:
            # Převede 1 na 'o ' a 0 na '  '
            line = "".join(
                [self.live_char if cell == 1 else self.dead_char for cell in row]
            )
            output.append(padding + line)

        # Spodní ohraničení
        output.append(padding + separator)

        # Patička a info
        output.append(
            f"Dimensions: {self.height}x{self.width} | Generation: {self.generation}"
        )
        output.append(f"(Press Ctrl+C to stop)")

        # Vrátí Rich Text objekt pro plynulý tisk
        return Text("\n".join(output))

    def _get_live_neighbor_count(self) -> np.ndarray:
        """
        Vypočítá počet živých sousedů pro každou buňku pomocí 2D konvoluce SciPy.
        Používá 'wrap' pro okraje (toroidní pole), stejně jako v C kódu.
        """
        # 3x3 jádro (kernel), které vylučuje středovou buňku
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)

        # Konvoluce s 'wrap' pro toroidní pole
        neighbor_counts = convolve2d(
            self.grid, kernel, mode="same", boundary="wrap"
        ).astype(np.int8)
        return neighbor_counts

    def next_generation(self):
        """
        Vypočítá další stav mřížky na základě Conwayových pravidel.
        (Stejná logika jako v C kódu, ale s použitím NumPy/SciPy pro efektivitu)
        """
        neighbors = self._get_live_neighbor_count()

        # Přežití: Živá buňka (1) A 2 nebo 3 sousedi
        survival_mask = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))

        # Reprodukce: Mrtvá buňka (0) A přesně 3 sousedi
        reproduction_mask = (self.grid == 0) & (neighbors == 3)

        # Nový stav mřížky je sjednocení masek pro přežití a reprodukci
        self.grid = (survival_mask | reproduction_mask).astype(np.int8)
        self.generation += 1

    def run_simulation(self):
        """Spustí hlavní smyčku simulace s plynulým Rich Live renderingem."""

        self.console.print("🚀 Starting Conway's Game of Life - Blinker...")
        time.sleep(1)  # Krátká pauza pro úvodní zprávu

        try:
            # Rich Live objekt spravuje plynulé překreslování
            with Live(self.get_grid_text(), console=self.console, screen=True) as live:
                # Nastavíme 'screen=True' pro lepší konzolový efekt (vymaže předchozí obsah)
                while True:
                    # 1. Vypočítáme stav nové generace a zvýšíme počítadlo
                    self.next_generation()

                    # 2. Aktualizujeme Rich Live objekt novým obsahem
                    live.update(self.get_grid_text())

                    # 3. time.sleep řídí rychlost simulace
                    time.sleep(self.delay_seconds)

        except KeyboardInterrupt:
            self.console.print("\nSimulation terminated by user (Ctrl+C).")
        except Exception as e:
            self.console.print(f"\nAn error occurred: {e}")


# --- Hlavní Spouštěcí Blok ---
if __name__ == "__main__":

    # Inicializace s výchozími rozměry 15x7 a zpožděním 0.5s
    game = GameOfLife()

    # Inicializace - vzor BLINKER
    # C kód: current_grid[3][7] = 1; current_grid[3][8] = 1; current_grid[3][9] = 1;
    # (řádek 3, sloupce 7, 8, 9)
    # Rozměry: 7 řádků (0-6), 15 sloupců (0-14).
    # Středový řádek je index 3. Sloupce 7, 8, 9 jsou na střed.

    initial_blinker_pattern = [(3, 7), (3, 8), (3, 9)]

    game.set_initial_pattern(initial_blinker_pattern)

    # Spuštění simulace
    game.run_simulation()
