# Opening Animation Skip Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a responsive two-key opening animation skip flow.

**Architecture:** Keep skip state in a small Pygame-independent module. Replace
opening-only blocking waits with a frame-based helper that polls events and
redraws the active opening frame.

**Tech Stack:** Python, Pygame, unittest

---

### Task 1: Two-Step Skip State

**Files:**
- Create: `opening_skip.py`
- Create: `tests/test_opening_skip.py`

- [x] **Step 1: Write the failing state tests**

Test that the first key reveals the prompt without skipping, and the second key
returns a skip request that remains active.

- [x] **Step 2: Verify the tests fail**

Run `python -m unittest tests.test_opening_skip -v` and confirm the module is
missing.

- [x] **Step 3: Implement `OpeningSkipState`**

Add `prompt_visible`, `skipped`, and `press_key()` with the two-step transition.

- [x] **Step 4: Verify the tests pass**

Run `python -m unittest tests.test_opening_skip -v`.

### Task 2: Responsive Opening Flow

**Files:**
- Modify: `main.py:621`

- [x] **Step 1: Add opening event and frame helpers**

Poll `QUIT` and `KEYDOWN`, draw the prompt at the bottom of the screen, and
wait through short 60 FPS frame loops instead of `pygame.time.wait()`.

- [x] **Step 2: Integrate every opening phase**

Use the same state through story typing, story pauses, credit fades, and final
pauses. Stop opening audio and return immediately when the second key is
pressed.

- [x] **Step 3: Run regression verification**

Run the opening tests, existing non-image tests, `python -m py_compile`, and
`git diff --check`.
