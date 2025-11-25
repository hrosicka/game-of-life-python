import numpy as np
import time
import os

# --- Constants --- 
WIDTH = 30  # Number of columns in the grid
HEIGHT = 15 # Number of rows in the grid
DELAY_SECONDS = 1.0 # Delay between generations

# --- Function to clear the screen ---
def clear_screen():
    """Clears the console (uses 'cls' for Windows, 'clear' otherwise)."""
    # Uses 'os.name' to detect the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Function to print the grid ---
def print_grid(grid):
    """Prints the current state of the grid to the console."""
    clear_screen()
    print("Conway's Game of Life")
    print("-" * (WIDTH * 2))
    
    # Iterate over rows
    for row in grid:
        # Convert 1 to 'o' (live cell) and 0 to ' ' (dead cell)
        line = "".join(['o ' if cell == 1 else '  ' for cell in row])
        print(line)
    
    print("-" * (WIDTH * 2))
    print(f"Dimensions: {HEIGHT}x{WIDTH}")

# --- Function to count neighbors ---
def count_live_neighbors(grid, x, y):
    """
    Counts the number of live neighbors for a given cell (x=row, y=column).
    Uses wrap-around logic for connecting the edges (toroidal field).
    """
    count = 0
    
    # Iterate over the 3x3 surrounding area
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the current cell
            if i == 0 and j == 0:
                continue

            # Calculate the neighbor's position with wrapping
            neighbor_x = (x + i + HEIGHT) % HEIGHT
            neighbor_y = (y + j + WIDTH) % WIDTH

            # NumPy array is indexed [row][column]
            if grid[neighbor_x][neighbor_y] == 1:
                count += 1
    return count

# --- Function to calculate the next generation ---
def next_generation(current_grid):
    """
    Calculates the state of the grid for the next generation based on Conway's rules.
    """
    # Create a new grid to store the next generation's state
    # (important: a copy initialized to zeros, so we don't modify the current state)
    next_grid = np.zeros((HEIGHT, WIDTH), dtype=int)

    # Iterate over every cell
    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_live_neighbors(current_grid, i, j)
            is_alive = current_grid[i][j] == 1

            # Apply Conway's rules
            if is_alive:
                # 1. Death by underpopulation or overpopulation (<2 or >3 neighbors)
                if neighbors < 2 or neighbors > 3:
                    next_grid[i][j] = 0
                # 2. Survival (2 or 3 neighbors)
                else:
                    next_grid[i][j] = 1
            else:
                # 4. Reproduction (exactly 3 neighbors)
                if neighbors == 3:
                    next_grid[i][j] = 1
                # 5. Stays dead
                else:
                    next_grid[i][j] = 0
                    
    return next_grid

# --- Main execution function ---
def main():
    """Sets up the game and runs the main simulation loop."""
    
    # Create the initial grid (all cells are dead, 0)
    # Use NumPy for efficient matrix operations
    current_grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # --- Initialization ---
    # Set up initial patterns (TOAD oscillators)

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
    
    # --- Main simulation loop ---
    try:
        while True:
            # 1. Display the current state
            print_grid(current_grid)

            # 2. Calculate and get the next generation
            current_grid = next_generation(current_grid)

            # 3. Delay for visualization
            time.sleep(DELAY_SECONDS)
            
    except KeyboardInterrupt:
        # Allows for graceful program termination by pressing Ctrl+C
        print("\nSimulation terminated by user.")
        
# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()