import numpy as np
import time
import os

# --- Konfigurace ---
# Změňte 'cls' na 'clear' pro Linux/macOS, pokud to používáte
CLEAR_COMMAND = 'cls' 

WIDTH = 60      # Počet sloupců v mřížce
HEIGHT = 30     # Počet řádků v mřížce
DELAY_MS = 100  # Zpoždění v milisekundách pro každou generaci (původně 0, ale pro viditelnou simulaci je potřeba)
DELAY_S = DELAY_MS / 1000.0 # Převod na sekundy

# Pulsar pattern - ofsety buněk (řádek, sloupec)
PULSAR_PATTERN = np.array([
    [1, 3], [1, 4], [1, 5],
    [1, 9], [1, 10], [1, 11],
    [3, 1], [3, 6], [3, 8], [3, 13],
    [4, 1], [4, 6], [4, 8], [4, 13],
    [5, 1], [5, 6], [5, 8], [5, 13],
    [6, 3], [6, 4], [6, 5],
    [6, 9], [6, 10], [6, 11],
    [8, 3], [8, 4], [8, 5],
    [8, 9], [8, 10], [8, 11],
    [9, 1], [9, 6], [9, 8], [9, 13],
    [10, 1], [10, 6], [10, 8], [10, 13],
    [11, 1], [11, 6], [11, 8], [11, 13],
    [13, 3], [13, 4], [13, 5],
    [13, 9], [13, 10], [13, 11],
])

# --- Funkce ---

def count_live_neighbors(grid: np.ndarray, x: int, y: int) -> int:
    """
    Spočítá počet živých sousedů pro danou buňku.
    Používá cyklické obcházení všech 8 sousedů.
    """
    count = 0
    # Iteruje přes sousedy v okolí 3x3
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Přeskoč vlastní buňku
            if i == 0 and j == 0:
                continue

            neighbor_x = x + i
            neighbor_y = y + j

            # Kontrola hranic
            if 0 <= neighbor_x < HEIGHT and 0 <= neighbor_y < WIDTH:
                if grid[neighbor_x, neighbor_y] == 1:
                    count += 1
    return count

def print_grid(grid: np.ndarray):
    """
    Vytiskne aktuální mřížku do konzole po vymazání obrazovky.
    """
    os.system(CLEAR_COMMAND) 
    
    # Rychlejší tisk mřížky
    output = ""
    for row in grid:
        # Převedení pole čísel na řetězec 'X' a ' '
        output += "".join(['X' if cell == 1 else ' ' for cell in row]) + "\n"
    print(output, end='')

def place_pattern(grid: np.ndarray, pattern: np.ndarray, start_x: int, start_y: int):
    """
    Umístí zadaný vzor na mřížku na specifikované místo.
    """
    for x_offset, y_offset in pattern:
        x = start_x + x_offset
        y = start_y + y_offset

        if 0 <= x < HEIGHT and 0 <= y < WIDTH:
            grid[x, y] = 1

def update_grid(current_grid: np.ndarray) -> np.ndarray:
    """
    Vypočítá další generaci na základě pravidel Hry života.
    """
    # Vytvoření nové mřížky pro další generaci
    next_grid = np.zeros((HEIGHT, WIDTH), dtype=int)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_live_neighbors(current_grid, i, j)

            is_alive = current_grid[i, j] == 1

            if is_alive:
                # 1. & 3. Živá buňka s < 2 nebo > 3 sousedy umírá
                if neighbors == 2 or neighbors == 3:
                    next_grid[i, j] = 1  # 2. Přežívá
                else:
                    next_grid[i, j] = 0  # Umírá
            else:
                # 4. Mrtvá buňka s přesně 3 sousedy ožívá
                if neighbors == 3:
                    next_grid[i, j] = 1  # Ožívá (reprodukce)
                else:
                    next_grid[i, j] = 0  # Zůstává mrtvá
    
    return next_grid

# --- Hlavní smyčka ---

def main():
    """
    Hlavní simulační smyčka.
    """
    # Inicializace mřížky s nulami
    current_grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # Umístění Pulsar vzoru
    start_row = 10
    start_col = 20
    place_pattern(current_grid, PULSAR_PATTERN, start_row, start_col)
    
    print(f"Spouštění simulace Conwayovy hry života (Pulsar) v Pythonu.")
    print(f"Velikost mřížky: {HEIGHT}x{WIDTH}, Zpoždění: {DELAY_MS}ms. Stiskněte Ctrl+C pro ukončení.")
    time.sleep(2) # Malé zpoždění před startem

    try:
        while True:
            # 1. Zobrazení aktuální mřížky
            print_grid(current_grid)

            # 2. Výpočet další generace
            current_grid = update_grid(current_grid)

            # 4. Zpoždění pro vizualizaci
            time.sleep(DELAY_S)
            
    except KeyboardInterrupt:
        # Ukončení programu po stisku Ctrl+C
        print("\nSimulace byla ukončena uživatelem.")
        
if __name__ == "__main__":
    # Kontrola, zda je nainstalován numpy (nutné)
    try:
        import numpy
    except ImportError:
        print("Chyba: Kód vyžaduje knihovnu numpy. Nainstalujte ji pomocí: pip install numpy")
        exit(1)
        
    main()