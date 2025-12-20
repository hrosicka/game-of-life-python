# python -m pytest -q
from pathlib import Path
import importlib.util
import numpy as np
import numpy.testing as npt

def load_game_class(relpath: str):
    """
    Dynamically load a GameOfLife class from a source file in the repo root.

    relpath is relative to the repository root (tests/ is one level below),
    e.g. 'game-of-life-blinker.py'
    """
    repo_root = Path(__file__).parent.parent
    src_path = repo_root / relpath
    assert src_path.exists(), f"Source file not found: {src_path}"
    # create a safe module name
    mod_name = "gomodule_" + src_path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(src_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GameOfLife

def test_blinker_oscillation_period_2():
    Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 5, "height": 5, "delay_seconds": 0.0})
    # Horizontal blinker centered at row=2, cols=1..3
    game.set_initial_pattern([(2,1), (2,2), (2,3)])
    before = game.grid.copy()
    # 1st step -> vertical
    game.next_generation()
    expected1 = np.zeros((5,5), dtype=np.int8)
    expected1[1,2] = 1
    expected1[2,2] = 1
    expected1[3,2] = 1
    npt.assert_array_equal(game.grid, expected1)
    # 2nd step -> back to horizontal (period 2)
    game.next_generation()
    npt.assert_array_equal(game.grid, before)

def test_toad_oscillation_period_2():
    Game = load_game_class("game-of-life-toad.py")
    game = Game({"width": 6, "height": 6, "delay_seconds": 0.0})
    # Toad initial configuration (classic)
    # Three in row at (2,2),(2,3),(2,4) and three at (3,1),(3,2),(3,3)
    coords = [(2,2),(2,3),(2,4),(3,1),(3,2),(3,3)]
    game.set_initial_pattern(coords)
    before = game.grid.copy()
    game.next_generation()
    game.next_generation()
    # After two generations the toad should return to its initial pattern
    npt.assert_array_equal(game.grid, before)

def test_beacon_oscillation_period_2():
    Game = load_game_class("game-of-life-beacon.py")
    game = Game({"width": 8, "height": 8, "delay_seconds": 0.0})
    # Beacon pattern: two 2x2 blocks touching diagonally
    coords = [
        (0,0),(0,1),(1,0),(1,1),  # top-left block
        (2,2),(2,3),(3,2),(3,3)   # bottom-right block (touching diagonally)
    ]
    game.set_initial_pattern(coords, row_offset=1, col_offset=1)  # move away from border
    before = game.grid.copy()
    game.next_generation()
    game.next_generation()
    # Beacon is a period-2 oscillator - after 2 steps it should be the same
    npt.assert_array_equal(game.grid, before)

def test_set_initial_pattern_ignores_out_of_bounds():
    Game = load_game_class("game-of-life-blinker.py")
    game = Game({"width": 3, "height": 3, "delay_seconds": 0.0})
    # Provide coordinates, some outside the 3x3 grid
    coords = [(-1,0), (0,0), (0,3), (3,3)]
    game.set_initial_pattern(coords)
    # Only (0,0) should have been set
    expected = np.zeros((3,3), dtype=np.int8)
    expected[0,0] = 1
    npt.assert_array_equal(game.grid, expected)

def test_get_grid_text_contains_generation_and_dimensions():
    Game = load_game_class("game-of-life-toad.py")
    game = Game({"width": 6, "height": 4, "delay_seconds": 0.0})
    txt = game.get_grid_text()
    # get_grid_text should return a rich.text.Text object or string-like with generation info
    s = str(txt)
    assert "Generation" in s or "Generation:" in s or "Generation" in s
    assert "Dimensions" in s or "Dimensions:" in s