# HUD Safe Zone Gameplay Area Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep all active gameplay entities below the top HUD/Boss UI safe zone.

**Architecture:** Add shared safe-zone constants in `config.py`, compress top UI geometry in `ui.py`, and replace hard-coded top-screen gameplay bounds in `player.py` and `enemy.py` with `GAMEPLAY_TOP`.

**Tech Stack:** Python, Pygame, `unittest`.

---

### Task 1: Shared Safe-Zone Constants

**Files:**
- Modify: `config.py`
- Test: `tests/test_hud_safe_zone.py`

- [ ] Add tests that assert `HUD_HEIGHT == 52`, `BOSS_BAR_HEIGHT == 30`, and `GAMEPLAY_TOP == 82`.
- [ ] Add constants in `config.py` immediately after `SCREEN_WIDTH, SCREEN_HEIGHT`.
- [ ] Run `python -m unittest tests.test_hud_safe_zone`.

### Task 2: Compact UI Geometry

**Files:**
- Modify: `ui.py`
- Test: `tests/test_ui.py`

- [ ] Update HUD geometry tests to require all status rects inside `0..HUD_HEIGHT`.
- [ ] Update Boss bar geometry tests to require the Boss bar inside `HUD_HEIGHT..GAMEPLAY_TOP`.
- [ ] Compress `gameplay_hud_rects()` and `draw_boss_health_bar()` to fit the safe zone.
- [ ] Run `python -m unittest tests.test_ui tests.test_boss_health`.

### Task 3: Gameplay Entity Top Bounds

**Files:**
- Modify: `player.py`
- Modify: `enemy.py`
- Test: `tests/test_hud_safe_zone.py`

- [ ] Add tests that instantiate `Player`, regular `Enemy_1`, and Boss classes and verify their top positions respect `GAMEPLAY_TOP`.
- [ ] Clamp player movement top to `GAMEPLAY_TOP`.
- [ ] Spawn regular enemies and Bosses at `GAMEPLAY_TOP`.
- [ ] Update Boss top-edge movement checks to use `GAMEPLAY_TOP`.
- [ ] Run `python -m unittest tests.test_hud_safe_zone`.

### Task 4: Verification

**Files:**
- Compile: `config.py`, `ui.py`, `player.py`, `enemy.py`, `main.py`, new tests

- [ ] Run non-Pillow tests with Python 3.12.
- [ ] Run Pillow-dependent tests with the bundled runtime.
- [ ] Run `py_compile`.
- [ ] Run `git diff --check`.
