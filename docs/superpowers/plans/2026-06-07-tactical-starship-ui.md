# Tactical Starship UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the approved Tactical Starship visual system to every menu and the gameplay HUD without changing game behavior.

**Architecture:** Add a presentation-only `ui.py` module with deterministic geometry helpers and reusable Pygame drawing primitives. Keep navigation, progression, events, and game state in `main.py`; replace only its direct UI drawing calls with shared helpers.

**Tech Stack:** Python 3.12, Pygame 2.6.1, `unittest`, existing `font.ttf`

---

## File Structure

- Create `ui.py`: theme constants, geometry, font cache, panels, buttons, headings, stat cards, HUD, slider, and modal backdrop.
- Create `tests/test_ui.py`: geometry, semantic style, and headless rendering tests.
- Modify `main.py`: use the shared UI across gameplay and all menu/result screens.
- Modify `.gitignore`: ignore visual brainstorming artifacts.

### Task 1: Geometry And Theme Contract

**Files:**
- Create: `tests/test_ui.py`
- Create: `ui.py`

- [ ] **Step 1: Write failing geometry tests**

Add tests asserting that `level_grid_rects(600, 900)` returns 15 unique
three-column rectangles within the screen and that
`gameplay_hud_rects(600)` returns four non-overlapping rectangles.

- [ ] **Step 2: Verify the tests fail**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_ui -v
```

Expected: import failure because `ui.py` does not exist.

- [ ] **Step 3: Implement minimal geometry and theme constants**

Create `ui.py` with `COLORS`, `level_grid_rects()`, and
`gameplay_hud_rects()`. Geometry functions return `pygame.Rect` instances and
do not initialize a display.

- [ ] **Step 4: Verify geometry tests pass**

Run the same command. Expected: all geometry tests pass.

### Task 2: Shared Tactical Drawing Primitives

**Files:**
- Modify: `tests/test_ui.py`
- Modify: `ui.py`

- [ ] **Step 1: Write failing rendering tests**

Use `SDL_VIDEODRIVER=dummy`, initialize Pygame, render a panel, each semantic
button style, HUD, and slider to an alpha surface, and assert that drawing
changes representative pixels without exceeding surface bounds.

- [ ] **Step 2: Verify the new tests fail**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_ui -v
```

Expected: failures for missing drawing helpers.

- [ ] **Step 3: Implement reusable UI primitives**

Add:

- `get_font(size)`
- `draw_text(...)`
- `draw_panel(...)`
- `draw_button(...)`
- `draw_heading(...)`
- `draw_stat_card(...)`
- `draw_gameplay_hud(...)`
- `draw_slider(...)`
- `draw_modal_backdrop(...)`

Use alpha overlays, cyan borders, clipped corners, warm gold coin accents,
muted red danger styling, hover emphasis, and disabled styling.

- [ ] **Step 4: Verify UI tests pass**

Run the same test command. Expected: all UI tests pass with dummy video.

### Task 3: Main Menu, Level Selection, And Hard Mode

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Import the shared UI module**

Import named helpers from `ui.py` while retaining the existing global
`font` for opening-animation compatibility.

- [ ] **Step 2: Replace main-menu drawing**

Keep the existing scrolling background, button actions, and click rectangles.
Render a dark central command panel, tactical heading, cyan primary Play
button, secondary buttons, and muted red Exit button with hover states.

- [ ] **Step 3: Replace level selectors**

Use `level_grid_rects()` for levels 1-15, a three-column grid, locked styles,
and a shared Back button. Preserve current unlock checks and actions.

- [ ] **Step 4: Compile and smoke-test imports**

Run:

```powershell
.\.venv\Scripts\python.exe -m py_compile ui.py main.py
```

Expected: exit code 0.

### Task 4: Upgrade, Settings, Credits, And Pause

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Restyle Upgrade**

Keep current costs and purchase logic. Draw the coin balance in a stat card
and render three upgrade cards with level, effect name, cost, affordability,
hover state, and a shared Back button.

- [ ] **Step 2: Restyle Settings**

Keep control-mode cycling and volume calculations. Render both controls inside
a tactical panel and use `draw_slider()` for the volume control.

- [ ] **Step 3: Restyle Credits and Pause**

Use modal panels, consistent headings, grouped credit rows, and shared tactical
buttons while preserving current actions.

- [ ] **Step 4: Run UI and existing tests**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: all tests pass.

### Task 5: Results Screens And Gameplay HUD

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Restyle game-over and completion screens**

Use the modal backdrop, tactical heading, and styled keyboard instructions.
Preserve existing keys and music.

- [ ] **Step 2: Restyle stage-clear screen**

Keep score animation and returned actions. Replace raw rectangles with shared
primary, secondary, and danger button styles.

- [ ] **Step 3: Replace gameplay text**

Replace four direct `display_text()` calls with
`draw_gameplay_hud(screen, level, score, player.lives, player.coin)`.

- [ ] **Step 4: Run complete verification**

Run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m py_compile ui.py main.py
git diff --check
```

Expected: all tests pass, compilation succeeds, and no whitespace errors are
reported.

### Task 6: Visual Smoke Verification

**Files:**
- No production file changes expected.

- [ ] **Step 1: Run a dummy-driver render smoke**

Render representative menu, upgrade, settings, result modal, and gameplay HUD
surfaces without entering the main game loop. Expected: no Pygame exceptions.

- [ ] **Step 2: Inspect repository state**

Run:

```powershell
git status --short
git diff -- main.py ui.py tests/test_ui.py .gitignore
```

Confirm that the user's pre-existing `level = 15` change remains and that no
temporary preview artifacts are tracked.
