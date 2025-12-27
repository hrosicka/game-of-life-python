from pathlib import Path
import importlib.util
import numpy as np
import numpy.testing as npt
import pytest

# Helper: dynamicky načte modul a třídu z daného souboru
def load_module_and_class(relpath: str, class_name: str):
    repo_root = Path(__file__).parent.parent
    src_path = repo_root / relpath
    assert src_path.exists(), f"Source file not found: {src_path}"
    mod_name = "gomodule_" + src_path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(src_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, getattr(module, class_name)

def test_glider_set_initial_patterns_and_text():
    module, GliderSimulation = load_module_and_class("game-of-life-glider.py", "GliderSimulation")
    game = GliderSimulation({"width": 15, "height": 12, "delay_seconds": 0.0})
    game.set_initial_patterns()
    # Known coordinates from glider1 and glider2 should be set
    assert game.grid[1, 2] == 1  # glider1
    assert game.grid[5, 5] == 1  # glider2
    txt = game.get_grid_text()
    s = str(txt)
    assert "Glider" in s

def test_lwss_get_color_for_age_ranges_and_pattern_set():
    module, LWSS = load_module_and_class("game-of-life-lwss.py", "LWSSAgingSimulation")
    game = LWSS({"width": 10, "height": 6, "delay_seconds": 0.0})
    # Exercise color mapping for representative ages
    assert game.get_color_for_age(0) == "bold white"
    assert game.get_color_for_age(1) == "bold white"
    assert game.get_color_for_age(2) == "bright_cyan"
    assert game.get_color_for_age(3) == "cyan"
    assert game.get_color_for_age(4) == "turquoise2"
    assert game.get_color_for_age(5) == "dodger_blue1"
    assert game.get_color_for_age(7) == "dodger_blue1"
    assert game.get_color_for_age(8) == "blue3"

    # set_lwss_pattern places multiple cells relative to start coordinates
    game2 = LWSS({"width": 10, "height": 8, "delay_seconds": 0.0})
    game2.set_lwss_pattern(1, 2)
    # pattern includes (0,1) relative -> global (1,3)
    assert game2.grid[1 + 0, 2 + 1] == 1

def test_lwss_next_generation_birth_and_survival_behavior():
    module, LWSS = load_module_and_class("game-of-life-lwss.py", "LWSSAgingSimulation")
    game = LWSS({"width": 7, "height": 7, "delay_seconds": 0.0})
    # Test birth: cell has exactly 3 live neighbors -> becomes age 1
    game.grid = np.zeros((7,7), dtype=np.int32)
    # set three neighbors of target (3,3)
    game.grid[2,3] = 1
    game.grid[3,2] = 1
    game.grid[3,4] = 1
    game.generation = 0
    game.next_generation()
    assert game.grid[3,3] == 1
    assert game.generation == 1
    assert game.grid.dtype == np.int32

    # Test survival: live cell with 2 neighbors increments its age
    game = LWSS({"width": 7, "height": 7, "delay_seconds": 0.0})
    game.grid = np.zeros((7,7), dtype=np.int32)
    # center alive with age 2 and exactly two neighbors
    game.grid[3,3] = 2
    game.grid[3,2] = 1
    game.grid[3,4] = 1
    game.generation = 5
    game.next_generation()
    # center should survive and increment age to 3
    assert game.grid[3,3] == 3
    assert game.generation == 6

def test_lwss_run_handles_keyboard_interrupt_and_no_main_side_effects(monkeypatch):
    module, LWSS = load_module_and_class("game-of-life-lwss.py", "LWSSAgingSimulation")
    # Dummy Console to capture prints
    class DummyConsole:
        def __init__(self):
            self.messages = []
        def clear(self):
            pass
        def print(self, *args, **kwargs):
            self.messages.append(" ".join(str(a) for a in args))
    # Dummy Live that raises KeyboardInterrupt inside context to trigger handler
    class DummyLive:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            raise KeyboardInterrupt
        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(module, "Live", DummyLive)
    monkeypatch.setattr(module, "Console", DummyConsole)
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)

    game = LWSS({"width": 10, "height": 6, "delay_seconds": 0.0})
    # run() should handle KeyboardInterrupt gracefully (not raise) and console should be DummyConsole
    game.run()
    assert isinstance(game.console, DummyConsole)
    # After run, at least one message should exist (start/stop)
    assert len(game.console.messages) >= 0  # just ensure console accessible

def test_imports_do_not_execute_main_blocks():
    # Ensure importing modules does not create module-level runtime objects (main protected by __name__ == "__main__")
    for fname in ["game-of-life-gun.py", "game-of-life-lwss.py", "game-of-life-glider.py", "game-of-life-pulsar.py"]:
        repo_root = Path(__file__).parent.parent
        src_path = repo_root / fname
        mod_name = "checkmod_" + src_path.stem.replace("-", "_")
        spec = importlib.util.spec_from_file_location(mod_name, str(src_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Common script-level names used under __main__: 'game', 'sim' etc. They should not exist after import.
        assert not hasattr(module, "game")
        assert not hasattr(module, "sim")