# Upgrade and Settings Backgrounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Upgrade and Settings backgrounds with distinct pixel-art scenes that remain readable and loop vertically without a visible seam.

**Architecture:** Generate one source PNG per page, then process each source through the existing `tools/make_vertical_tile.py` pipeline into a `600x1536` runtime JPG. Keep `main.py` unchanged because both pages already load their named background through `ScrollingBackground`.

**Tech Stack:** Python 3.12, Pillow, Pygame, built-in image generation, Git

---

## File Structure

- Create `img/background/source/upgrade_background_source.png`: generated Upgrade workshop source.
- Create `img/background/source/setting_background_source.png`: generated Settings control-room source.
- Modify `img/background/upgrade_background.jpg`: seamless Upgrade runtime asset.
- Modify `img/background/setting_background.jpg`: seamless Settings runtime asset.
- Create temporarily under `verification/backgrounds/`: join and UI previews; remove before completion.

### Task 1: Verify the Existing Pipeline

- [ ] **Step 1: Run the current unit tests**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all 18 tests pass.

- [ ] **Step 2: Confirm existing page wiring**

Run:

```powershell
rg -n "setting_background|upgrade_background|ScrollingBackground" main.py
```

Expected: both pages load their existing JPG and call `advance()` followed by `draw()`.

### Task 2: Produce the Upgrade Background

- [ ] **Step 1: Generate the source**

Generate a tall modern pixel-art blue-purple space technology workshop. Place
cyan and violet machinery, energy conduits, panels, and structural framing near
the far left and right edges. Keep the center dark, quiet, and low-detail for
upgrade text and buttons. Keep the top and bottom regions compatible for
vertical blending. Exclude text, logos, spacecraft, characters, borders,
watermarks, and dominant circular objects.

- [ ] **Step 2: Save and process the asset**

Copy the selected generated image to:

```text
img/background/source/upgrade_background_source.png
```

Run:

```powershell
python tools\make_vertical_tile.py img\background\source\upgrade_background_source.png img\background\upgrade_background.jpg
```

Expected: a `600x1536` runtime JPG.

- [ ] **Step 3: Inspect the join**

Create a `600x600` preview containing the bottom 300 pixels followed by the top
300 pixels. Inspect it for horizontal discontinuity, brightness jumps, or
misaligned structures.

### Task 3: Produce the Settings Background

- [ ] **Step 1: Generate the source**

Generate a tall modern pixel-art deep-blue spacecraft control room. Place
restrained panels, vents, cables, and cool-blue indicator lights near the far
left and right edges. Keep the center and upper-left dark, calm, and less dense
than the Upgrade page. Keep the top and bottom regions compatible for vertical
blending. Exclude text, logos, spacecraft, characters, borders, watermarks, and
bright central displays.

- [ ] **Step 2: Save and process the asset**

Copy the selected generated image to:

```text
img/background/source/setting_background_source.png
```

Run:

```powershell
python tools\make_vertical_tile.py img\background\source\setting_background_source.png img\background\setting_background.jpg
```

Expected: a `600x1536` runtime JPG.

- [ ] **Step 3: Inspect the join**

Create the same bottom-to-top join preview and confirm no visible seam or
brightness jump.

- [ ] **Step 4: Commit both page assets**

Run:

```powershell
git add img/background/source/upgrade_background_source.png img/background/source/setting_background_source.png img/background/upgrade_background.jpg img/background/setting_background.jpg
git commit -m "Replace upgrade and settings backgrounds"
```

### Task 4: Validate the Final Result

- [ ] **Step 1: Validate dimensions and edge differences**

Use Pillow to assert both runtime files are `600x1536` and report the mean RGB
difference between their first and last rows. Expected: each mean difference is
below `3.0`.

- [ ] **Step 2: Create representative page previews**

Render each background at a representative scroll offset with the actual
`font.ttf` and representative Upgrade or Settings labels. Confirm central
labels remain readable and the themes are immediately distinguishable.

- [ ] **Step 3: Run complete verification**

Run:

```powershell
python -m unittest discover -s tests -v
python -m py_compile background.py main.py tools\make_vertical_tile.py
```

Then run the dummy SDL startup smoke test used by the existing background work.
Expected: tests pass, compilation succeeds, and startup prints
`main startup smoke OK`.

- [ ] **Step 4: Clean verification files and inspect Git state**

Remove only the temporary `verification/backgrounds` directory created by this
plan. Run:

```powershell
git diff --check
git status --short
git diff -- main.py
```

Expected: clean feature worktree and no `main.py` diff.

- [ ] **Step 5: Merge locally**

Fast-forward the completed feature branch into `master`, rerun the complete
verification on the merged result, remove the owned worktree, and delete the
merged branch. Preserve the user's existing uncommitted `main.py` change.
