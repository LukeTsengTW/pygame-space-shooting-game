# Auto-save Design

**Date:** 2026-06-08
**Status:** Approved (design)

## Goal

Add persistent save/load to the space shooter **without changing the existing
UI**. No new buttons, screens, or prompts — the game silently restores the
player's progress on launch and silently auto-saves at key moments.

Auto-save triggers:

1. The player closes the game — window-X, the menu Quit button, or any other
   normal exit path.
2. The player clicks a level (normal or hard campaign).
3. The player clears a stage.

A true force-kill (Task Manager / `SIGKILL` / power loss) cannot be intercepted
by any program; the level-click and stage-clear saves keep the file current so
at most the coins/score earned within the current in-progress run are lost.

## What gets saved

File: `%APPDATA%\SpaceShooter\savegame.json`

```json
{
  "version": 1,
  "progression": {
    "highest_unlocked_level": 1,
    "is_complete_game": false,
    "hard_level": 1
  },
  "economy": {
    "coin": 0,
    "damage_level": 0,
    "bullet_speed_level": 0,
    "live_level": 0
  },
  "settings": {
    "volume_level": 0.5,
    "control_mode": 0
  }
}
```

### Source of truth: levels, not effects

The upgrade **costs** and **effect values** are NOT stored. They are recomputed
from the upgrade levels on load, using the exact formulas the in-game store
already uses, so stored data can never drift out of sync with effects:

| Derived value          | Formula                                  |
| ---------------------- | ---------------------------------------- |
| `damage_level_need_coin`        | `damage_level * 1234`           |
| `bullet_speed_level_need_coin`  | `bullet_speed_level * 321`      |
| `live_level_need_coin`          | `live_level * 5432`             |
| `player.damage`                 | `50 + damage_level` (base 50)   |
| `max_lives`                     | `10 + live_level` (base 10)     |
| `BULLET_SPEED`                  | `20 + bullet_speed_level` (base 20) |

> The base values (50 / 10 / 20) match `Player.__init__` (`self.damage = 50`)
> and `config.py` (`max_lives = 10`, `BULLET_SPEED = 20`). The store increments
> each by `+1` per level, so `base + level` reproduces the in-session result
> exactly.
>
> Pre-existing quirk, out of scope: the projectile-speed upgrade mutates
> `main.BULLET_SPEED`, but bullet velocity is read from `player.py`'s own
> `BULLET_SPEED` (a separate binding created by `from config import *`), so the
> upgrade has limited runtime effect today. To preserve current behavior
> exactly, restore reproduces the store's behavior (sets `main.BULLET_SPEED`)
> and does NOT attempt to "fix" the cross-module binding.

`settings` (master volume + keyboard/cursor control mode) is included for
continuity. It is low-cost and harmless; the loader tolerates its absence.

## Components

### New module: `save_manager.py` (pure, unit-testable)

No `pygame` or `config` import — safe to import in isolation, like
`level_progress.py`. Operates purely on a plain `dict` so it can be tested
without pygame.

```
resolve_save_path() -> str
    %APPDATA%\SpaceShooter\savegame.json
    Falls back to <cwd>/savegame.json when APPDATA is unset (tests / non-Windows).
    Accepts an optional override for tests.

DEFAULT_STATE -> dict
    The full default structure shown above.

load_state(path=None) -> dict
    Reads + JSON-parses the file, then deep-merges over DEFAULT_STATE so missing
    or older-version keys fall back to defaults. Tolerant: a missing file,
    corrupt JSON, or wrong types returns DEFAULT_STATE. Never raises.

save_state(state, path=None) -> bool
    Creates the parent directory, writes atomically (temp file in the same dir +
    os.replace), returns True on success. Swallows IO/OS errors and returns
    False so a failed save can never crash the game.
```

### Glue in `main.py` (the only edits to `main.py`)

These live in `main.py` because they touch its module globals, the `config`
globals, and the `player` instance:

```
gather_save_state() -> dict
    Reads the live state (highest_unlocked_level, is_complete_game, hard_level,
    player.coin, damage_level, bullet_speed_level, live_level, volume_level,
    player.control) into the save dict.

apply_save_state(data) -> None
    Writes the dict back into the live globals, mirroring exactly what the
    upgrade store / settings screen do:
      - global highest_unlocked_level, hard_level, is_complete_game
      - global damage_level, bullet_speed_level, live_level
      - global damage_level_need_coin, bullet_speed_level_need_coin,
        live_level_need_coin  (recomputed from levels)
      - global max_lives, BULLET_SPEED  (recomputed from levels)
      - player.coin, player.damage, player.lives, player.control
      - volume_level + pygame.mixer.music.set_volume(...)

autosave() -> None
    save_manager.save_state(gather_save_state())
```

## Data flow

```
startup:  load_state() --> apply_save_state(data)        (once, after Player created)
exit:     atexit --> autosave()                          (covers all normal exits)
level:    chose_level / chose_hard_level --> autosave()  (after level chosen)
clear:    stage clear block --> autosave()               (after progression update)
```

### Trigger wiring

- **Startup:** after `player = Player()` (~`main.py:71-73`), call
  `apply_save_state(save_manager.load_state())`.
- **Exit:** `atexit.register(autosave)` registered once at startup. `atexit`
  fires on normal interpreter exit, including `sys.exit()` — which every
  `pygame.QUIT` handler, the menu Quit button (`sys.exit` action), and the
  bottom-of-file shutdown all call. One registration covers them all.
- **Level click:** in `chose_level` (after `level = i`, ~`main.py:341`) and
  `chose_hard_level` (after `hard_level = i`, ~`main.py:413`), call `autosave()`.
- **Stage clear:** in the stage-clear block, right after
  `highest_unlocked_level = unlocked_level_after_clear(...)` and the
  `is_complete_game = True` update (~`main.py:1039-1043`), call `autosave()`.

## Error handling

- `load_state` never raises: missing file, unreadable file, corrupt JSON, or
  wrong-typed values all degrade to defaults (fresh-game state).
- `save_state` never raises: directory-creation or write failures are swallowed
  and return `False`. A save failure must never interrupt gameplay or exit.
- Atomic write (temp + `os.replace`) guarantees the existing save is never left
  half-written if the process dies mid-write.

## Testing

`tests/test_save_manager.py` — pure module, uses a tmp path override, no pygame:

- No file present -> `load_state` returns `DEFAULT_STATE`.
- `save_state` then `load_state` round-trips an arbitrary state unchanged.
- Corrupt JSON file -> `load_state` returns defaults.
- Partial / missing-keys / older-`version` file -> merged over defaults
  (present keys kept, missing keys defaulted).
- `save_state` writes atomically and leaves no leftover temp file in the dir.
- `resolve_save_path` honors `APPDATA` and falls back when it is unset.

`main.py` glue (`gather_save_state` / `apply_save_state`) is not unit-tested
directly because importing `main.py` launches the game (consistent with the
existing "no test imports main" convention). Its correctness is covered by the
pure `save_manager` tests plus manual verification.

## Out of scope

- No save UI (slots, continue button, delete-save). Single implicit save.
- No migration framework beyond the version-aware default merge.
- No fix for the pre-existing cross-module `BULLET_SPEED` binding quirk.
- No saving of mid-run transient state (current score, in-progress level
  position, live sprites). Saves capture progression + economy + settings only.
