import json
import os

import save_manager


def test_load_returns_defaults_when_no_file(tmp_path):
    path = str(tmp_path / "missing.json")
    assert save_manager.load_state(path) == save_manager.DEFAULT_STATE


def test_resolve_path_uses_appdata(monkeypatch):
    monkeypatch.setenv("APPDATA", os.path.join("X", "Roaming"))
    expected = os.path.join("X", "Roaming", "SpaceShooter", "savegame.json")
    assert save_manager.resolve_save_path() == expected


def test_resolve_path_falls_back_without_appdata(monkeypatch):
    monkeypatch.delenv("APPDATA", raising=False)
    assert save_manager.resolve_save_path() == os.path.join(os.getcwd(), "savegame.json")


def test_corrupt_json_returns_defaults(tmp_path):
    path = tmp_path / "save.json"
    path.write_text("{ not valid json", encoding="utf-8")
    assert save_manager.load_state(str(path)) == save_manager.DEFAULT_STATE


def test_partial_file_merges_over_defaults(tmp_path):
    path = tmp_path / "save.json"
    path.write_text(
        json.dumps({"progression": {"highest_unlocked_level": 7}}),
        encoding="utf-8",
    )
    state = save_manager.load_state(str(path))
    assert state["progression"]["highest_unlocked_level"] == 7
    assert state["progression"]["hard_level"] == 1  # defaulted
    assert state["economy"]["coin"] == 0  # whole section defaulted


def test_wrong_types_fall_back_to_defaults(tmp_path):
    path = tmp_path / "save.json"
    path.write_text(json.dumps({"economy": {"coin": "lots"}}), encoding="utf-8")
    state = save_manager.load_state(str(path))
    assert state["economy"]["coin"] == 0
