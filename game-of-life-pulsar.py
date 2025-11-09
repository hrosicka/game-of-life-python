import numpy as np
import time
import os

# --- Configuration ---
# Change 'cls' to 'clear' for Linux/macOS if you are using it
CLEAR_COMMAND = 'cls' 

WIDTH = 60      # Number of columns in the grid
HEIGHT = 30     # Number of rows in the grid
DELAY_MS = 100  # Delay in milliseconds for each generation (originally 0, but needed for visible simulation)
DELAY_S = DELAY_MS / 1000.0 # Conversion to seconds

# Pulsar pattern - cell offsets (row, column)
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

# --- Functions ---

def count_live_neighbors(grid: np.ndarray, x: int, y: int) -> int:
    """
    Counts the number of live neighbors for a given cell.
    Uses cyclic iteration over all 8 neighbors.
    """
    count = 0
    # Iterate over neighbors in the 3x3 area
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Skip the cell itself
            if i == 0 and j == 0:
                continue

            neighbor_x = x + i
            neighbor_y = y + j

            # Boundary check
            if 0 <= neighbor_x < HEIGHT and 0 <= neighbor_y < WIDTH:
                if grid[neighbor_x, neighbor_y] == 1:
                    count += 1
    return count

def print_grid(grid: np.ndarray):
    """
    Prints the current grid to the console after clearing the screen.
    """
    os.system(CLEAR_COMMAND) 
    
    # Faster grid printing
    output = ""
    for row in grid:
        # Convert array of numbers to a string of 'X' and ' '
        output += "".join(['X' if cell == 1 else ' ' for cell in row]) + "\n"
    print(output, end='')

def place_pattern(grid: np.ndarray, pattern: np.ndarray, start_x: int, start_y: int):
    """
    Places the specified pattern onto the grid at the given location.
    """
    for x_offset, y_offset in pattern:
        x = start_x + x_offset
        y = start_y + y_offset

        if 0 <= x < HEIGHT and 0 <= y < WIDTH:
            grid[x, y] = 1

def update_grid(current_grid: np.ndarray) -> np.ndarray:
    """
    Calculates the next generation based on the Game of Life rules.
    """
    # Create a new grid for the next generation
    next_grid = np.zeros((HEIGHT, WIDTH), dtype=int)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = count_live_neighbors(current_grid, i, j)

            is_alive = current_grid[i, j] == 1

            if is_alive:
                # 1. & 3. A live cell with < 2 or > 3 neighbors dies
                if neighbors == 2 or neighbors == 3:
                    next_grid[i, j] = 1  # 2. Continues living
                else:
                    next_grid[i, j] = 0  # Dies
            else:
                # 4. A dead cell with exactly 3 neighbors comes to life
                if neighbors == 3:
                    next_grid[i, j] = 1  # Becomes alive (reproduction)
                else:
                    next_grid[i, j] = 0  # Remains dead
    
    return next_grid

# --- Main Loop ---

def main():
    """
    Main simulation loop.
    """
    # Initialize the grid with zeros
    current_grid = np.zeros((HEIGHT, WIDTH), dtype=int)
    
    # Place the Pulsar pattern
    start_row = 10
    start_col = 20
    place_pattern(current_grid, PULSAR_PATTERN, start_row, start_col)
    
    print(f"Starting Conway's Game of Life (Pulsar) simulation in Python.")
    print(f"Grid size: {HEIGHT}x{WIDTH}, Delay: {DELAY_MS}ms. Press Ctrl+C to stop.")
    time.sleep(2) # Small delay before start

    try:
        while True:
            # 1. Display the current grid
            print_grid(current_grid)

            # 2. Calculate the next generation
            current_grid = update_grid(current_grid)

            # 4. Delay for visualization
            time.sleep(DELAY_S)
            
    except KeyboardInterrupt:
        # Program termination upon pressing Ctrl+C
        print("\nSimulation terminated by user.")
        
if __name__ == "__main__":
    # Check if numpy is installed (required)
    try:
        import numpy
    except ImportError:
        print("Error: This code requires the numpy library. Install it using: pip install numpy")
        exit(1)
        
    main()