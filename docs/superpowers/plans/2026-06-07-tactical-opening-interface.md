# Tactical Opening Interface Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the plain black opening sequence with a Tactical Starship communications interface and translate its skip prompt to English.

**Architecture:** Add deterministic opening render helpers to `ui.py`; keep event processing, audio, timing, typewriter state, and fade loops in `main.py`. Extend the existing headless Pygame UI tests and preserve `OpeningSkipState` unchanged.

**Tech Stack:** Python 3.12, Pygame 2.6.1, `unittest`, existing `font.ttf`

---

## File Structure

- Modify `ui.py`: tactical starfield, briefing frame, skip strip, creator card.
- Modify `tests/test_ui.py`: deterministic and bounded opening-render tests.
- Modify `tests/test_opening_skip.py`: exact English prompt contract.
- Modify `opening_skip.py`: exported English prompt constant.
- Modify `main.py`: use opening UI helpers without changing timing or skip flow.

### Task 1: Opening UI Contract

**Files:**
- Modify: `tests/test_ui.py`
- Modify: `tests/test_opening_skip.py`

- [ ] **Step 1: Write failing tests**

Add tests for deterministic starfield pixels, briefing rendering at steps 1
and 11, non-empty creator card alpha, skip strip drawing, and exact
`PRESS ANY KEY AGAIN TO SKIP` prompt text.

- [ ] **Step 2: Verify tests fail**

Run:

```powershell
python -m unittest tests.test_ui tests.test_opening_skip -v
```

Expected: import failures for the new functions and prompt constant.

### Task 2: Tactical Opening Primitives

**Files:**
- Modify: `ui.py`
- Modify: `opening_skip.py`

- [ ] **Step 1: Add the prompt constant**

Export:

```python
OPENING_SKIP_PROMPT = "PRESS ANY KEY AGAIN TO SKIP"
```

- [ ] **Step 2: Implement deterministic render helpers**

Add:

- `draw_tactical_starfield(surface, tick)`
- `draw_opening_briefing(surface, text, step, total_steps, tick)`
- `draw_opening_skip_prompt(surface, prompt)`
- `create_creator_card(size)`

Use fixed arithmetic star positions, cut-corner panels, cyan scan lines,
briefing status labels, progress bars, and existing font helpers.

- [ ] **Step 3: Verify focused tests pass**

Run the focused test command again. Expected: all tests pass.

### Task 3: Opening Flow Integration

**Files:**
- Modify: `main.py`

- [ ] **Step 1: Import the new UI helpers and prompt**

Import the prompt from `opening_skip.py` and rendering helpers from `ui.py`.
Remove the local Chinese prompt constant.

- [ ] **Step 2: Route story frames through the briefing renderer**

Pass current sentence index and total count through
`display_text_word_by_word()` and `draw_opening_text()`. Use
`pygame.time.get_ticks()` for visual animation only.

- [ ] **Step 3: Route the visible skip prompt through the status-strip renderer**

Keep `skip_state.prompt_visible` and all event semantics unchanged.

- [ ] **Step 4: Replace creator text with the card surface**

Fade the entire creator card while retaining current alpha steps, wait
durations, early skip returns, and music-stop behavior.

### Task 4: Verification

**Files:**
- No additional production files expected.

- [ ] **Step 1: Run focused and complete tests**

Run:

```powershell
python -m unittest tests.test_ui tests.test_opening_skip -v
python -m unittest tests.test_background tests.test_level_progress tests.test_opening_skip tests.test_ui -v
```

- [ ] **Step 2: Run compilation and diff checks**

Run:

```powershell
python -m py_compile ui.py opening_skip.py main.py tests\test_ui.py
git diff --check
```

- [ ] **Step 3: Produce visual previews**

Render a partial briefing frame, completed frame with skip prompt, and creator
card to ignored `.superpowers/previews/` files. Inspect text fit, contrast,
scan-line placement, and consistency with the existing Tactical Starship UI.
