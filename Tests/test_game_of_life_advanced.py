from pathlib import Path
import importlib.util
import numpy as np
import numpy.testing as npt

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

def test_block_still_life_beacon():
    # Block 2x2 should remain unchanged after next_generation
    module, Game = load_game_class("game-of-life-beacon.py")
    game = Game({"width": 6, "height": 6, "delay_seconds": 0.0})
    # Place 2x2 block at (1,1),(1,2),(2,1),(2,2)
    coords = [(1,1),(1,2),(2,1),(2,2)]
    game.set_initial_pattern(coords, row_offset=0, col_offset=0)
    before = game.grid.copy()
    game.next_generation()
    npt.assert_array_equal(game.grid, before)

def test_multiple_set_initial_pattern_accumulates_blinker():
    # Calling set_initial_pattern multiple times adds cells (doesn't reset grid)
    module, Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 5, "height": 5, "delay_seconds": 0.0})
    game.set_initial_pattern([(0,0)])   # first call
    game.set_initial_pattern([(4,4)])   # second call
    expected = np.zeros((5,5), dtype=np.int8)
    expected[0,0] = 1
    expected[4,4] = 1
    npt.assert_array_equal(game.grid, expected)

def test_custom_live_dead_chars_in_output_toad():
    # Ensure get_grid_text uses configured live/dead characters
    module, Game = load_game_class("game-of-life-toad.py")
    game = Game({"width": 6, "height": 4, "delay_seconds": 0.0, "live_cell_char": "X", "dead_cell_char": "."})
    # set one cell alive to see 'X' in output
    game.set_initial_pattern([(1,1)])
    txt = game.get_grid_text()
    s = str(txt)
    assert "X" in s
    assert "." in s  # dead char should also appear

def test_dimensions_preserved_after_next_generation():
    # Grid shape should remain identical after generation step
    module, Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 7, "height": 3, "delay_seconds": 0.0})
    before_shape = game.grid.shape
    game.next_generation()
    assert game.grid.shape == before_shape

def test_run_simulation_performs_n_steps_and_stops(monkeypatch):
    # Use a Dummy Live that raises an exception after N updates to stop the loop.
    module, Game = load_game_class("game-of-life-beacon.py")
    N = 3
    class DummyLive:
        def __init__(self, initial_text, console=None):
            self.count = 0
        def __enter__(self):
            return self
        def update(self, new_text):
            # next_generation is called before update, so count will reflect iterations
            self.count += 1
            if self.count >= N:
                # raise to break out of simulation loop; run_simulation catches Exception
                raise RuntimeError("stop-after-n")
        def __exit__(self, exc_type, exc, tb):
            # Don't suppress exceptions here; outer try/except in run_simulation will handle it
            return False

    # Patch Live and time.sleep
    monkeypatch.setattr(module, "Live", DummyLive)
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    game = Game({"width": 6, "height": 6, "delay_seconds": 0.0})
    # initialize with at least one live cell to make next_generation meaningful
    game.set_initial_pattern([(2,2)])
    start_gen = game.generation
    # run_simulation should finish (handle exception internally) and return without raising
    game.run_simulation()
    # generation should have advanced at least N times (or exactly N depending on ordering)
    assert game.generation >= start_gen + N

def test_grid_dtype_preserved_after_next_generation():
    module, Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 4, "height": 4, "delay_seconds": 0.0})
    assert game.grid.dtype == np.int8
    game.next_generation()
    assert game.grid.dtype == np.int8