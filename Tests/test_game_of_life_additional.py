from pathlib import Path
import importlib.util
import numpy as np
import numpy.testing as npt
import types

# --- Helper to dynamically load GameOfLife class from repo files ---
def load_game_class(relpath: str):
    repo_root = Path(__file__).parent.parent
    src_path = repo_root / relpath
    assert src_path.exists(), f"Source file not found: {src_path}"
    mod_name = "gomodule_" + src_path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(src_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.GameOfLife

# --- Additional tests ---

def test_neighbor_counts_fill_boundary_beacon():
    # Beacon file uses 'fill' mode (no wrap). A single live cell in corner
    module, Game = load_game_class("game-of-life-beacon.py")
    game = Game({"width": 3, "height": 3, "delay_seconds": 0.0})
    # Single live cell at top-left corner
    game.grid = np.zeros((3,3), dtype=np.int8)
    game.grid[0,0] = 1
    neighbors = game._get_live_neighbor_count()
    # Positions (0,1),(1,0),(1,1) should each see 1 neighbor, others 0, and (0,0) should be 0
    expected = np.zeros((3,3), dtype=np.int8)
    expected[0,1] = 1
    expected[1,0] = 1
    expected[1,1] = 1
    npt.assert_array_equal(neighbors, expected)

def test_neighbor_counts_wrap_boundary_toad():
    # Toad file uses 'wrap' mode (toroidal). Cells at opposite edges count as neighbors.
    module, Game = load_game_class("game-of-life-toad.py")
    game = Game({"width": 5, "height": 3, "delay_seconds": 0.0})
    game.grid = np.zeros((3,5), dtype=np.int8)
    # Place live cells at (0,0) and (0,4) (left and right edges)
    game.grid[0,0] = 1
    game.grid[0,4] = 1
    neighbors = game._get_live_neighbor_count()
    # Because of wrapping, cell (0,0) has neighbor at (0,4) and vice versa.
    # Check some relevant positions:
    # - (0,0) neighbors should include (0,4) and (0,1) and below cells if present; since only two cells set,
    #   neighbors for (0,0) should be 1 (from (0,4))
    assert neighbors[0,0] >= 1
    # - cell (0,1) should see both (0,0) and possibly (0,4) via wrap around adjacency horizontally (depends on kernel).
    assert neighbors[0,1] >= 1
    # At least ensure wrapping made nonzero neighbor counts near edges
    assert neighbors.sum() >= 2

def test_next_generation_rules_basic_cases():
    # Test survival (2 neighbors), reproduction (3 neighbors) and overpopulation (>3 dies)
    module, Game = load_game_class("game-of-life-beacon.py")
    game = Game({"width": 5, "height": 5, "delay_seconds": 0.0})
    # Center cell indices
    r, c = 2, 2

    # 1) Survival: center alive with exactly 2 neighbors -> stays alive
    game.grid = np.zeros((5,5), dtype=np.int8)
    game.grid[r, c] = 1
    game.grid[r, c-1] = 1
    game.grid[r, c+1] = 1
    game.generation = 0
    game.next_generation()
    assert game.grid[r, c] == 1
    assert game.generation == 1

    # 2) Reproduction: center dead with exactly 3 neighbors -> becomes alive
    game.grid = np.zeros((5,5), dtype=np.int8)
    game.grid[r-1, c] = 1
    game.grid[r, c-1] = 1
    game.grid[r, c+1] = 1
    game.generation = 10
    game.next_generation()
    assert game.grid[r, c] == 1
    assert game.generation == 11

    # 3) Overpopulation: live cell with 4 neighbors -> dies
    game.grid = np.zeros((5,5), dtype=np.int8)
    game.grid[r, c] = 1
    # four neighbors
    game.grid[r-1, c] = 1
    game.grid[r+1, c] = 1
    game.grid[r, c-1] = 1
    game.grid[r, c+1] = 1
    game.generation = 0
    game.next_generation()
    assert game.grid[r, c] == 0

def test_grid_dtype_and_generation_increment():
    module, Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 4, "height": 4, "delay_seconds": 0.0})
    assert game.grid.dtype == np.int8
    start_gen = game.generation
    game.next_generation()
    assert game.generation == start_gen + 1

def test_get_grid_text_content_and_structure_for_blinker():
    module, Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 6, "height": 4, "delay_seconds": 0.0})
    txt = game.get_grid_text()
    s = str(txt)
    # Header expected
    assert "Conway" in s
    assert "Blinker" in s
    # The separator line length should match approx width*2 from blinker formatting
    assert "-" in s

def test_set_initial_pattern_with_offset_beacon():
    module, Game = load_game_class("game-of-life-beacon.py")
    game = Game({"width": 10, "height": 10, "delay_seconds": 0.0})
    coords = [(0,0), (0,1), (1,0), (1,1)]
    # Place block with offsets
    game.set_initial_pattern(coords, row_offset=3, col_offset=4)
    # The block should appear at (3,4),(3,5),(4,4),(4,5)
    expected = np.zeros((10,10), dtype=np.int8)
    expected[3,4] = 1
    expected[3,5] = 1
    expected[4,4] = 1
    expected[4,5] = 1
    npt.assert_array_equal(game.grid, expected)

def test_run_simulation_handles_keyboard_interrupt(monkeypatch):
    # Replace Live with a dummy context manager that raises KeyboardInterrupt on enter
    module, Game = load_game_class("game-of-life-beacon.py")
    class DummyLive:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            raise KeyboardInterrupt
        def __exit__(self, exc_type, exc, tb):
            return False
    monkeypatch.setattr(module, "Live", DummyLive)
    # patch time.sleep to avoid delays
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    game = Game({"width": 6, "height": 6, "delay_seconds": 0.0})
    # run_simulation should handle KeyboardInterrupt and return without raising
    game.run_simulation()
