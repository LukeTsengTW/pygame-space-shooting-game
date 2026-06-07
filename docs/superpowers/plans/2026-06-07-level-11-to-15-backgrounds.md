# Level 11 To 15 Pixel Backgrounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, process, and verify five distinct vertically seamless pixel-art backgrounds for Levels 11 through 15.

**Architecture:** Each level receives an independently generated source PNG and a processed `600x1536` JPEG through the existing vertical tile pipeline. Existing automated validation checks dimensions, JPEG edge continuity, and Pygame viewport coverage, while join and gameplay previews verify perspective, central readability, and Level 15 boss-arena spacing.

**Tech Stack:** Built-in image generation, Python 3.12, Pillow 12, Pygame 2.6.1, existing `tools/make_vertical_tile.py`, existing `tools/validate_level_backgrounds.py`, `unittest`.

---

## File Structure

- Create `img/background/source/lv11_background_source.png` through `lv15_background_source.png`.
- Modify `img/background/lv11_background.jpg` through `lv15_background.jpg`.
- Create temporary join and gameplay previews under `verification/backgrounds/`, then remove them before completion.
- Do not modify `main.py`; its existing uncommitted changes belong to the user.
- Do not modify gameplay, enemies, bosses, or UI.

### Task 1: Verify The Existing Background Pipeline

**Files:**
- Verify: `tools/make_vertical_tile.py`
- Verify: `tools/validate_level_backgrounds.py`
- Verify: `tests/test_vertical_tile.py`
- Verify: `tests/test_level_background_validation.py`

- [ ] **Step 1: Run the existing processing and validation tests**

Run:

```powershell
python -m unittest tests.test_vertical_tile tests.test_level_background_validation -v
```

Expected: all existing processing and validation tests pass.

- [ ] **Step 2: Validate an approved existing asset**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 10 --end-level 10
```

Expected:

```text
img\background\lv10_background.jpg: size=600x1536, edge_mean=<3.0, viewport=covered
```

- [ ] **Step 3: Confirm no runtime code changes are required**

Run:

```powershell
git diff -- main.py
```

Record that any displayed `main.py` diff existed before this phase and must remain untouched.

### Task 2: Generate And Process Levels 11 To 13

**Files:**
- Create: `img/background/source/lv11_background_source.png`
- Create: `img/background/source/lv12_background_source.png`
- Create: `img/background/source/lv13_background_source.png`
- Modify: `img/background/lv11_background.jpg`
- Modify: `img/background/lv12_background.jpg`
- Modify: `img/background/lv13_background.jpg`

- [ ] **Step 1: Generate Level 11**

Use built-in image generation:

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down gameplay background for Level 11
Primary request: the cratered surface of the Moon viewed directly from straight overhead
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft; clearly pixel art, not photorealistic
Camera/perspective: strict nadir top-down orthographic aerial view, like a vertical scrolling game map; no horizon, no vanishing point, no side-view landscape
Composition/framing: tall portrait approximately 600:1536; gray craters, fractured regolith, boulders, and shadowed ridges concentrated along the far left and right sides; a darker smooth lunar valley or regolith plain forms the central combat corridor
Lighting/mood: cold quiet lunar terrain, neutral gray with blue-black shadows and pale silver highlights
Constraints: top 12% and bottom 12% have compatible crater density, texture, color, and brightness; central 50% and upper-left HUD region remain dark; no flags, landers, footprints, bases, mission equipment, text, UI, logo, border, signature, or watermark
Avoid: horizon, isometric view, photorealism, giant central crater, bright white center, recognizable human equipment
```

- [ ] **Step 2: Generate Level 12**

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down gameplay background for Level 12
Primary request: Mercury's heat-scorched cratered surface viewed directly from straight overhead
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft; clearly pixel art, not photorealistic
Camera/perspective: strict nadir top-down orthographic aerial view, like a vertical scrolling game map; no horizon, no vanishing point
Composition/framing: tall portrait approximately 600:1536; crater fields, fractured plains, ridges, and heat-darkened rocks concentrated along both sides; a smoother dark central combat corridor
Lighting/mood: harsh solar illumination, gray-brown and charcoal rock with restrained gold-white highlights and deep black shadows
Constraints: visually warmer and harsher than Level 11; top 12% and bottom 12% have compatible crater density and lighting; keep central 50% and upper-left HUD dark; no equipment, text, UI, logo, border, signature, or watermark
Avoid: horizon, isometric view, photorealism, giant Sun, lava, giant central crater, bright center
```

- [ ] **Step 3: Generate Level 13**

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down gameplay background for Level 13
Primary request: the canyon and dust terrain of Mars viewed directly from straight overhead
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft; clearly pixel art, not photorealistic
Camera/perspective: strict nadir top-down orthographic aerial view, like a vertical scrolling game map; no horizon, no skyline, no vanishing point
Composition/framing: tall portrait approximately 600:1536; red-orange canyon walls, eroded ridges, dark basalt, scattered rocks, and subtle dust patterns along both sides; a dark canyon floor or wind-cleared central flight corridor
Lighting/mood: muted rust, ochre, dark red, and violet-brown shadows at late dusk
Constraints: top 12% and bottom 12% have compatible canyon, dust, color, and brightness; central 50% and upper-left HUD remain dark; no bases, roads, vehicles, readable markings, text, UI, logo, border, signature, or watermark
Avoid: horizon, isometric view, photorealism, bright orange center, giant volcano, structures, aircraft
```

- [ ] **Step 4: Save and process Levels 11 to 13**

Copy the selected generated images to the source filenames above, then run:

```powershell
python tools/make_vertical_tile.py img/background/source/lv11_background_source.png img/background/lv11_background.jpg
python tools/make_vertical_tile.py img/background/source/lv12_background_source.png img/background/lv12_background.jpg
python tools/make_vertical_tile.py img/background/source/lv13_background_source.png img/background/lv13_background.jpg
```

- [ ] **Step 5: Validate Levels 11 to 13**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 11 --end-level 13
```

Expected: three successful validations with `600x1536`, edge mean at or below `3.0`, and `viewport=covered`.

- [ ] **Step 6: Create and inspect join previews**

For each level, create a `600x600` preview containing:

- Bottom 300 rows in the upper half.
- Top 300 rows in the lower half.

Reject an image if:

- A crater, ridge, or canyon is horizontally cut.
- A brightness band appears at the join.
- The perspective is not strict top-down.
- The center is too bright or crowded.

- [ ] **Step 7: Commit Levels 11 to 13**

```powershell
git add img/background/source/lv11_background_source.png img/background/source/lv12_background_source.png img/background/source/lv13_background_source.png img/background/lv11_background.jpg img/background/lv12_background.jpg img/background/lv13_background.jpg
git commit -m "Add seamless planetary backgrounds for levels 11 to 13"
```

### Task 3: Generate And Process Levels 14 And 15

**Files:**
- Create: `img/background/source/lv14_background_source.png`
- Create: `img/background/source/lv15_background_source.png`
- Modify: `img/background/lv14_background.jpg`
- Modify: `img/background/lv15_background.jpg`

- [ ] **Step 1: Generate Level 14**

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 14
Primary request: Jupiter's upper cloud layers viewed directly downward, with flowing orange and cream cloud bands and small vortices
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft; clearly pixel art, not photorealistic
Camera/perspective: direct downward atmospheric view with no horizon, no planet edge, and no side-view landscape
Composition/framing: tall portrait approximately 600:1536; orange, cream, tan, muted brown, and pale gold cloud streams flow vertically along the far left and right sides; small and medium vortices remain near the edges; a darker calm atmospheric channel forms the central combat corridor
Lighting/mood: immense turbulent gas-giant atmosphere, dramatic but readable
Constraints: top 12% and bottom 12% have compatible vertical cloud flow, texture, color, and brightness; central 50% and upper-left HUD remain darker; no Great Red Spot, giant storm, lightning, stars, spacecraft, text, UI, logo, border, signature, or watermark
Avoid: horizontal bands, horizon, photorealism, giant circular vortex, bright white center, line-shaped storm effects
```

- [ ] **Step 2: Generate Level 15**

```text
Use case: stylized-concept
Asset type: vertical pixel-art boss gameplay background for Level 15
Primary request: a luminous galactic-core corridor with dense stellar clouds and star fields concentrated along both sides
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft; clearly pixel art, not photorealistic
Composition/framing: tall portrait approximately 600:1536; bright gold-white, cyan, violet, and restrained magenta stellar clouds along the far left and right sides; exceptionally wide black-navy central boss arena with the central 55% open
Lighting/mood: the most dramatic stage so far, immense galactic core energy with a calm readable center
Constraints: top 12% and bottom 12% have compatible star density, stellar-cloud texture, color, and brightness; upper-left HUD remains dark; no full spiral galaxy, black hole, giant star, dominant circular landmark, spacecraft, text, UI, logo, border, signature, or watermark
Avoid: photorealism, bright center, dense projectile-like stars in the central corridor, giant lens flare, central singularity
```

- [ ] **Step 3: Save and process Levels 14 and 15**

```powershell
python tools/make_vertical_tile.py img/background/source/lv14_background_source.png img/background/lv14_background.jpg
python tools/make_vertical_tile.py img/background/source/lv15_background_source.png img/background/lv15_background.jpg
```

- [ ] **Step 4: Validate Levels 14 and 15**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 14 --end-level 15
```

Expected: two successful validations.

- [ ] **Step 5: Inspect join previews**

Reject Level 14 if:

- Cloud bands create a horizontal tile line.
- A vortex is visibly cut at the join.
- The center is occupied by bright cream clouds.

Reject Level 15 if:

- The central 55% is not open.
- Stars resemble a dense projectile field in the center.
- The join cuts through a bright stellar landmark.

- [ ] **Step 6: Commit Levels 14 and 15**

```powershell
git add img/background/source/lv14_background_source.png img/background/source/lv15_background_source.png img/background/lv14_background.jpg img/background/lv15_background.jpg
git commit -m "Add seamless Jupiter and galactic backgrounds for levels 14 and 15"
```

### Task 4: Final Validation

**Files:**
- Verify: `img/background/lv11_background.jpg` through `lv15_background.jpg`
- Verify: `img/background/source/lv11_background_source.png` through `lv15_background_source.png`

- [ ] **Step 1: Run all unit tests**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass without warnings.

- [ ] **Step 2: Validate all five assets**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 11 --end-level 15
```

Expected: five successful validations.

- [ ] **Step 3: Compile actual Python files**

Run:

```powershell
python -m py_compile background.py main.py tools/__init__.py tools/make_vertical_tile.py tools/validate_level_backgrounds.py tests/__init__.py tests/test_background.py tests/test_vertical_tile.py tests/test_level_background_validation.py
```

Expected: exit code `0`.

- [ ] **Step 4: Run a dummy SDL startup smoke test**

Initialize Pygame with dummy video and audio drivers, bypass opening delays, post a `QUIT` event, and execute `main.py`.

Expected:

```text
main startup smoke OK
```

- [ ] **Step 5: Create gameplay previews**

For each Level 11 through Level 15:

- Draw the background at a representative offset on a `600x900` Pygame surface.
- Add the HUD and player ship.
- Save a temporary preview under `verification/backgrounds/`.
- Create a combined five-level montage.

Inspect:

- Moon, Mercury, and Mars are visually distinct.
- Levels 11 through 13 use strict top-down terrain views.
- Level 14 reads as Jupiter clouds rather than a terrestrial surface.
- Level 15 preserves the central Boss 3 arena.
- The HUD and player remain readable in every level.

- [ ] **Step 6: Remove verification previews and review Git state**

Run:

```powershell
git status --short
git diff --check
git diff -- main.py
```

Expected:

- Only intended source PNGs and runtime JPEGs are added or modified by this phase.
- `main.py` retains the user's pre-existing uncommitted changes and is not staged or committed.
