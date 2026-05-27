from pathlib import Path
import importlib.util
import numpy as np
import numpy.testing as npt
import pytest

# --- Helper to dynamically load GameOfLife class from repo files ---
def load_game_module_and_class(relpath: str):
    repo_root = Path(__file__).parent.parent
    src_path = repo_root / relpath
    assert src_path.exists(), f"Source file not found: {src_path}"
    mod_name = "gomodule_" + src_path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(src_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.GameOfLife

def test_wrap_vs_fill_boundary_behavior():
    # Prepare a corner-live-cell grid and compare neighbor counts between modules
    # Beacon uses 'fill' (no wrap), blinker uses 'wrap'. Ensure results differ for corner placement.
    beacon_mod, Beacon = load_game_module_and_class("game-of-life-beacon.py")
    blinker_mod, Blinker = load_game_module_and_class("game-of-life-blinker.py")
    # small grids for clarity
    b_game = Beacon({"width": 3, "height": 3, "delay_seconds": 0.0})
    bl_game = Blinker({"width": 3, "height": 3, "delay_seconds": 0.0})
    # place single live cell in top-left corner
    b_game.grid = np.zeros((3,3), dtype=np.int8); b_game.grid[0,0] = 1
    bl_game.grid = np.zeros((3,3), dtype=np.int8); bl_game.grid[0,0] = 1
    b_neighbors = b_game._get_live_neighbor_count()
    bl_neighbors = bl_game._get_live_neighbor_count()
    # For 'fill' mode (beacon) the opposite-corner neighbor should be zero, for 'wrap' might be non-zero
    # Specifically, for wrap the cell at (0,2) or (2,0) may see the corner due to wrapping.
    assert b_neighbors.sum() > 0  # some neighbors exist (adjacent)
    # At least one corresponding neighbor count should differ between fill and wrap
    assert not np.array_equal(b_neighbors, bl_neighbors)

def test_set_initial_pattern_with_offset_and_bounds_pulsar():
    pulsar_mod, Pulsar = load_game_module_and_class("game-of-life-pulsar.py")
    game = Pulsar({"width": 7, "height": 7, "delay_seconds": 0.0})
    # pattern coords include positions that, when offset, would fall partially outside
    coords = [(0, 0), (0, 6), (6, 0), (6, 6)]
    # Apply offset that would push some coords out of bounds; set_initial_pattern should ignore out-of-bounds silently
    game.set_initial_pattern(coords, row_offset=1, col_offset=1)
    # Only coords that fall inside should be set
    expected = np.zeros((7,7), dtype=np.int8)
    # (0,0) -> (1,1); (0,6)->(1,7) out of bounds; (6,0)->(7,1) out; (6,6)->(7,7) out
    expected[1,1] = 1
    npt.assert_array_equal(game.grid, expected)

def test_get_grid_text_formatting_variants():
    # Check get_grid_text returns strings containing expected decorative characters for each module
    files_and_expected = [
        ("game-of-life-blinker.py", "Blinker", "-"),
        ("game-of-life-toad.py", "Conway's Game of Life", "-"),
        ("game-of-life-beacon.py", "Beacon", "+"),  # beacon uses + and | borders
        ("game-of-life-pulsar.py", "Pulsar", "+"),
    ]
    for fname, expected_header, expected_border_char in files_and_expected:
        mod, Game = load_game_module_and_class(fname)
        game = Game({"width": 10, "height": 4, "delay_seconds": 0.0})
        # set one live cell to ensure live_char appears
        game.set_initial_pattern([(1,1)])
        txt = game.get_grid_text()
        s = str(txt)
        assert expected_header.split()[0] in s  # basic presence of header word
        assert expected_border_char in s

def test_run_simulation_handles_generic_exception_and_logs(monkeypatch):
    # Patch module.Live to raise a runtime error from __enter__ and ensure run_simulation catches it and prints
    beacon_mod, Beacon = load_game_module_and_class("game-of-life-beacon.py")

    # Dummy Console to capture messages
    class DummyConsole:
        def __init__(self):
            self.messages = []
        def print(self, *args, **kwargs):
            # store joined string
            self.messages.append(" ".join(str(x) for x in args))

    # Dummy Live that raises on enter
    class DummyLive:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            raise RuntimeError("simulated error")
        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(beacon_mod, "Live", DummyLive)
    # Patch Console in module before creating Game so constructor uses DummyConsole
    monkeypatch.setattr(beacon_mod, "Console", DummyConsole)
    # patch time.sleep to no-op
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    game = Beacon({"width": 6, "height": 6, "delay_seconds": 0.0})
    # run_simulation should not raise (it catches Exception) and should have logged the error
    # Since Console is dummy, its messages list should have one or two messages after run_simulation
    game.run_simulation()
    # the DummyConsole instance is assigned to game.console
    assert isinstance(game.console, DummyConsole)
    # There should be at least one message recorded (start message, or error)
    assert len(game.console.messages) >= 1

def test_run_simulation_update_loop_counts_steps(monkeypatch):
    # Patch Live.update to count updates and then raise to stop; ensure generation increments accordingly.
    blinker_mod, Blinker = load_game_module_and_class("game-of-life-blinker.py")

    class CountingLive:
        def __init__(self, initial, console=None, screen=False):
            self.count = 0
        def __enter__(self):
            return self
        def update(self, new_text):
            self.count += 1
            if self.count >= 4:
                # trigger an exception to exit loop (run_simulation catches and prints)
                raise RuntimeError("stop")
        def __exit__(self, exc_type, exc, tb):
            return False

    # Patch Live and time.sleep
    monkeypatch.setattr(blinker_mod, "Live", CountingLive)
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    # Patch Console to avoid real printing
    class DummyConsole:
        def print(self, *args, **kwargs):
            pass
    monkeypatch.setattr(blinker_mod, "Console", DummyConsole)

    game = Blinker({"width": 6, "height": 6, "delay_seconds": 0.0})
    # ensure at least one live cell so next_generation does something
    game.set_initial_pattern([(2,2)])
    start_gen = game.generation
    game.run_simulation()
    # After run_simulation, generation should have increased by at least the number of successful updates (>=4)
    assert game.generation >= start_gen + 4

def test_import_does_not_execute_main_block():
    # Importing the module should not run run_simulation (main guarded by __name__ == "__main__")
    # We'll dynamically import the file and ensure GameOfLife class exists and code didn't create a running object.
    mod, Game = load_game_module_and_class("game-of-life-pulsar.py")
    assert hasattr(mod, "GameOfLife")
    # No attribute like 'game' should exist at module-level (scripts create local variable only under main)
    assert not hasattr(mod, "game")