# HARD MODE — Design Spec

Date: 2026-06-08
Status: Approved (pending written-spec review)

## Goal

Make HARD MODE a real, playable difficulty. Hard mode uses the **same
scenes/levels** as normal mode, but each level is tougher:

- Every enemy (including bosses) has **3× HP**.
- Every enemy deals **3× contact damage** to the player.
- Enemies **spawn ~2× faster** (denser waves, sooner start).
- Boss **skill cooldowns are halved** (skills fire ~2× as often).

It must also actually wire selection → gameplay (currently broken) and
persist hard-campaign progress.

## Current state (why it's "unimplemented")

- `config.is_enter_hard_mode` exists but is always `False` and unused in
  the live flow.
- `chose_hard_level()` sets `hard_level = i` but **never sets `level`**, so
  the gameplay loop (which keys everything off `level`) never loads the
  selected hard level. Selecting a hard level effectively does nothing
  coherent.
- An abandoned stub multiplies HP by **20** in `Enemy_1/2/3` only, gated on
  an `is_enter_hard_mode` constructor param that nobody passes.
- Stage-clear always advances `highest_unlocked_level` (normal progression),
  so hard play would corrupt normal progression and never advance
  `hard_level`.

## Architecture note (wildcard-import gotcha)

Every module does `from config import *`, which **copies** bindings at import
time. Mutating `config.is_enter_hard_mode` is therefore NOT visible through a
module's wildcard-imported copy. The flag and tuning constants must be read as
**live module attributes** (`config.is_enter_hard_mode`, `config.HARD_*`)
wherever difficulty is applied. `main.py` and `enemy.py` will `import config`
explicitly (in addition to the existing `from config import *`).

## Tuning constants (config.py)

```python
is_enter_hard_mode = False          # existing flag, now the live source of truth

HARD_HP_MULTIPLIER = 3
HARD_DAMAGE_MULTIPLIER = 3
HARD_SPAWN_RATE_MULTIPLIER = 2      # enemy spawn probability ×2
HARD_START_DELAY_FACTOR = 0.5       # wave-start delay 3000ms → 1500ms
HARD_BOSS_COOLDOWN_FACTOR = 0.5     # boss skill cooldowns ×0.5
```

## Changes

### 1. Enemy/boss HP ×3 — centralized (enemy.py)

In `Enemy.__init__`, scale the incoming `hp` via the pure helper:

```python
self.hp = hard_mode.scale_hp(hp, config.is_enter_hard_mode)
```

All `Enemy_*` and `Boss_*` pass hp through `super().__init__`, so this one
spot covers the entire roster (verified). **Remove the ×20 stub** and the
`is_enter_hard_mode` constructor params from `Enemy_1/2/3`; HP scaling lives
only in the base.

### 2. Enemy → player damage ×3 (main.py)

After `enemy_damage_values` is built in the gameplay loop:

```python
enemy_damage_values = {
    k: hard_mode.scale_damage(v, config.is_enter_hard_mode)
    for k, v in enemy_damage_values.items()
}
```

### 3. Faster spawns ~2× (main.py)

- In `generate_enemy`, use an effective probability of
  `ENEMY_GENERATION_THRESHOLDS[enemy_type] * HARD_SPAWN_RATE_MULTIPLIER`
  when hard. (Doubling probability is what actually doubles density; the
  50ms gate is not the limiter.)
- Halve the wave-start delay: the `> 3000` check becomes
  `> 3000 * HARD_START_DELAY_FACTOR` when hard.

### 4. Boss cooldowns halved (enemy.py)

Add a helper that scales whichever cooldown attributes a boss defines:

```python
def apply_hard_boss_cooldowns(boss):
    for attr in ('laser_cooldown', 'scatter_cooldown',
                 'rapid_fire_cooldown', 'scatter_skill_cooldown'):
        if hasattr(boss, attr):
            setattr(boss, attr,
                    hard_mode.scale_boss_cooldown(getattr(boss, attr),
                                                  config.is_enter_hard_mode))
```

Call it at the end of each boss `__init__` (Boss_1/2/3), after the cooldowns
are assigned.

### 5. Mode entry + progression (main.py)

- `chose_level` level-select branch: `config.is_enter_hard_mode = False`.
- `chose_hard_level` level-select branch:
  `config.is_enter_hard_mode = True` and `level = i`. Stop reassigning the
  `hard_level` cap on selection.
- Stage clear (the `score > ...` block): when hard, advance the elite-campaign
  cap instead of the normal one, and autosave:
  ```python
  if config.is_enter_hard_mode:
      hard_level = unlocked_level_after_clear(hard_level, level)
  else:
      highest_unlocked_level = unlocked_level_after_clear(highest_unlocked_level, level)
  ```
  `hard_level` is already in the save schema, so autosave persists it.
- The `level > 15` completion branch:
  - Normal: unchanged (`is_complete_game = True` + `all_levels_completed_screen()`).
  - Hard: show a new `hard_campaign_completed_screen()` — an "ELITE CAMPAIGN
    COMPLETE" victory screen modeled on `all_levels_completed_screen()`
    (clickable + key `1` → main menu) — then return to menu. Does not touch
    `is_complete_game`.

Difficulty is only ever entered through these two selectors, so setting the
flag there fully determines the run; no reset needed elsewhere.

## Testability

Extract the difficulty arithmetic into a pure, pygame-free module
`hard_mode.py` (following `level_progress.py`):

```python
def scale_hp(base_hp, hard): ...
def scale_damage(base_damage, hard): ...
def scale_spawn_probability(p, hard): ...
def scale_boss_cooldown(cd, hard): ...
def scale_start_delay(delay, hard): ...
```

`enemy.py` / `main.py` call these (reading `config.is_enter_hard_mode` for the
`hard` arg). New `tests/test_hard_mode.py` asserts hard = 3×/2×/0.5× normal and
that `hard=False` is identity. Keeps the multipliers single-sourced and tested
without launching pygame.

## Out of scope

- Rebalancing individual enemy/boss values beyond the global multipliers.
- Separate hard-mode art/music.
- Difficulty settings UI beyond the existing NORMAL/HARD selectors.
