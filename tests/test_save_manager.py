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


def test_resolve_path_falls_back_without_appdata(monkeypatch, tmp_path):
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.chdir(tmp_path)
    assert save_manager.resolve_save_path() == os.path.join(str(tmp_path), "savegame.json")


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


def test_save_then_load_round_trips(tmp_path):
    path = str(tmp_path / "sub" / "save.json")  # parent dir does not exist yet
    state = save_manager.load_state(path)
    state["progression"]["highest_unlocked_level"] = 9
    state["progression"]["is_complete_game"] = True
    state["economy"]["coin"] = 12345
    state["economy"]["damage_level"] = 4
    state["settings"]["volume_level"] = 0.8
    assert save_manager.save_state(state, path) is True
    assert save_manager.load_state(path) == state


def test_save_leaves_no_temp_file(tmp_path):
    path = str(tmp_path / "save.json")
    assert save_manager.save_state(save_manager.DEFAULT_STATE, path) is True
    leftovers = [name for name in os.listdir(tmp_path) if name != "save.json"]
    assert leftovers == []


def test_save_returns_false_on_error(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("i am a file", encoding="utf-8")
    # Parent path is a regular file, so creating a dir/file under it must fail.
    path = str(blocker / "save.json")
    assert save_manager.save_state(save_manager.DEFAULT_STATE, path) is False


def test_save_returns_false_on_unserializable_state(tmp_path):
    path = str(tmp_path / "save.json")
    assert save_manager.save_state({"bad": object()}, path) is False
    assert not os.path.exists(path)
