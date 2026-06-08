"""Pure file-IO for the game save file. No pygame/config imports so it stays
unit-testable in isolation (like level_progress.py)."""

import json
import os
import tempfile

DEFAULT_STATE = {
    "version": 1,
    "progression": {
        "highest_unlocked_level": 1,
        "is_complete_game": False,
        "hard_level": 1,
    },
    "economy": {
        "coin": 0,
        "damage_level": 0,
        "bullet_speed_level": 0,
        "live_level": 0,
        "sentry_gun_level": 0,
        "tactical_support_level": 0,
    },
    "settings": {
        "volume_level": 0.5,
        "control_mode": 0,
        "opening_seen": False,
    },
}


def resolve_save_path(override=None):
    if override is not None:
        return override
    appdata = os.environ.get("APPDATA")
    if appdata:
        return os.path.join(appdata, "SpaceShooter", "savegame.json")
    return os.path.join(os.getcwd(), "savegame.json")


def _coerce(default_value, stored_value):
    # bool first: bool is a subclass of int, so check it before int/float.
    if isinstance(default_value, bool):
        return stored_value if isinstance(stored_value, bool) else default_value
    if isinstance(default_value, (int, float)):
        if isinstance(stored_value, (int, float)) and not isinstance(stored_value, bool):
            return stored_value
        return default_value
    if isinstance(default_value, str):
        return stored_value if isinstance(stored_value, str) else default_value
    return stored_value if stored_value is not None else default_value


def _merge(default, stored):
    if not isinstance(stored, dict):
        stored = {}
    result = {}
    for key, default_value in default.items():
        if isinstance(default_value, dict):
            result[key] = _merge(default_value, stored.get(key))
        else:
            result[key] = _coerce(default_value, stored.get(key))
    return result


def load_state(path=None):
    if path is None:
        path = resolve_save_path()
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        data = {}
    return _merge(DEFAULT_STATE, data)


def save_state(state, path=None):
    if path is None:
        path = resolve_save_path()
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=directory or None, suffix=".tmp")  # "" dirname -> None -> system temp dir
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(state, handle, indent=2)
            os.replace(tmp, path)
        except BaseException:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise
        return True
    except Exception:
        return False
