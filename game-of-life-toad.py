import numpy as np
import time
import os

# --- Konstanty ---
WIDTH = 30  # Počet sloupců v gridu
HEIGHT = 15 # Počet řádků v gridu
DELAY_SECONDS = 1.0 # Zpoždění mezi generacemi

# --- Funkce pro vymazání obrazovky ---
def clear_screen():
    """Vymaže konzoli (pro Windows použije 'cls', jinak 'clear')."""
    # Používá 'os.name' k detekci operačního systému
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Funkce pro tisk gridu ---
def print_grid(grid):
    """Vytiskne aktuální stav gridu do konzole."""
    clear_screen()
    print("Conway's Game of Life")
    print("-" * (WIDTH * 2))
    
    # Procházení řádků
    for row in grid:
        # Převod 1 na 'o' (živá buňka) a 0 na ' ' (mrtvá buňka)
        line = "".join(['o ' if cell == 1 else '  ' for cell in row])
        print(line)
    
    print("-" * (WIDTH * 2))
    print(f"Rozměry: {HEIGHT}x{WIDTH}")

# --- Funkce pro počítání sousedů ---
def count_live_neighbors(grid, x, y):
    """
    Spočítá počet živých sousedů pro danou buňku (x=řádek, y=sloupec).
    Používá logiku obtékání (wrap-around) pro propojení hran.
    """
    count = 0
    
    # Procházení okolí 3x3
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Přeskočení aktuální buňky
            if i == 0 and j == 0:
                continue

            # Výpočet pozice souseda s obtékáním (toroidní pole)
            neighbor_x = (x + i + HEIGHT) % HEIGHT
            neighbor_y = (y + j + WIDTH) % WIDTH

            # NumPy pole se indexuje [řádek][sloupec]
            if grid[neighbor_x][neighbor_y] == 1:
                count += 1
    return count

# --- Funkce pro výpočet další generace ---
def next_generation(current_grid):
    """
    Vypočítá stav gridu pro další generaci na základě Conwayových pravidel.
    """
    # Vytvoření nového gridu pro ukládání stavu další generace
    # (důležité: kopie s nulami, abychom nemodifikovali aktuální stav)
    next_grid = np.zeros((HEIGHT, WIDTH), dtype=int)

    # Procházení každé buňky
    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_live_neighbors(current_grid, i, j)
            is_alive = current_grid[i][j] == 1

            # Aplikace Conwayových pravidel
            if is_alive:
                # 1. Smrt kvůli pod/přemnožení (<2 nebo >3 sousedé)
                if neighbors < 2 or neighbors > 3:
                    next_grid[i][j] = 0
                # 2. Přežití (2 nebo 3 sousedé)
                else:
                    next_grid[i][j] = 1
            else:
                # 4. Oživení (přesně 3 sousedé)
                if neighbors == 3:
                    next_grid[i][j] = 1
                # 5. Zůstává mrtvá
                else:
                    next_grid[i][j] = 0
                    
    return next_grid

# --- Hlavní spouštěcí funkce ---
def main():
    """Nastaví hru a spustí hlavní simulační smyčku."""
    
    # Vytvoření počátečního gridu (všechny buňky jsou mrtvé, 0)
    # Použití NumPy pro efektivní práci s maticemi
    current_grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # --- Inicializace ---
    # Nastavení počátečních vzorů (TOAD oscilátory)

    # TOAD 1
    current_grid[5, 10] = 1
    current_grid[5, 11] = 1
    current_grid[5, 12] = 1
    current_grid[6, 9]  = 1
    current_grid[6, 10] = 1
    current_grid[6, 11] = 1

    # TOAD 2
    current_grid[10, 12] = 1
    current_grid[10, 13] = 1
    current_grid[10, 14] = 1
    current_grid[11, 11] = 1
    current_grid[11, 12] = 1
    current_grid[11, 13] = 1
    
    # --- Hlavní smyčka simulace ---
    try:
        while True:
            # 1. Zobrazení aktuálního stavu
            print_grid(current_grid)

            # 2. Výpočet a získání další generace
            current_grid = next_generation(current_grid)

            # 3. Zpoždění pro vizualizaci
            time.sleep(DELAY_SECONDS)
            
    except KeyboardInterrupt:
        # Umožní elegantní ukončení programu stiskem Ctrl+C
        print("\nSimulace ukončena uživatelem.")
        
# Spuštění hlavní funkce, pokud je skript spuštěn přímo
if __name__ == "__main__":
    main()