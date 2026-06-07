# Level 2 To 10 Pixel Backgrounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate, process, and verify nine distinct vertically seamless pixel-art backgrounds for Levels 2 through 10.

**Architecture:** Each level receives an independently generated source PNG and a processed `600x1536` JPEG produced by the existing vertical tile tool. A focused asset validator checks expected files, dimensions, JPEG edge continuity, and Pygame viewport coverage, while visual join previews verify that numerical continuity does not hide broken landmarks.

**Tech Stack:** Built-in image generation, Python 3.12, Pillow 12, Pygame 2.6.1, `unittest`, existing `tools/make_vertical_tile.py`.

---

## File Structure

- Create `tools/validate_level_backgrounds.py`: validates source/runtime asset presence, dimensions, edge difference, and Pygame draw coverage.
- Create `tests/test_level_background_validation.py`: test-first coverage for validator behavior.
- Create `img/background/source/lv2_background_source.png` through `lv10_background_source.png`: generated source artwork.
- Modify `img/background/lv2_background.jpg` through `lv10_background.jpg`: processed runtime assets.
- Create temporary `verification/backgrounds/` join and gameplay previews during validation, then remove them before commit.
- Do not modify `main.py`, because it already loads `lv1_background.jpg` through `lv20_background.jpg` by filename.

### Task 1: Add A Level Background Asset Validator

**Files:**
- Create: `tests/test_level_background_validation.py`
- Create: `tools/validate_level_backgrounds.py`

- [ ] **Step 1: Write failing tests for asset inspection**

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.validate_level_backgrounds import inspect_background


class LevelBackgroundValidationTests(unittest.TestCase):
    def test_inspect_background_reports_size_and_edge_difference(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            path = Path(directory) / "background.jpg"
            image = Image.new("RGB", (600, 1536), (5, 10, 20))
            image.save(path, quality=92, subsampling=0)

            result = inspect_background(path)

            self.assertEqual(result["size"], (600, 1536))
            self.assertEqual(result["edge_mean"], 0)

    def test_inspect_background_rejects_wrong_dimensions(self):
        with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
            path = Path(directory) / "background.jpg"
            Image.new("RGB", (600, 900), (5, 10, 20)).save(path)

            with self.assertRaisesRegex(ValueError, "expected 600x1536"):
                inspect_background(path)
```

- [ ] **Step 2: Run the tests and verify the import failure**

Run:

```powershell
python -m unittest tests.test_level_background_validation -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'tools.validate_level_backgrounds'`.

- [ ] **Step 3: Implement the minimal inspection function**

```python
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


EXPECTED_SIZE = (600, 1536)


def inspect_background(path):
    path = Path(path)
    with Image.open(path) as source:
        image = source.convert("RGB")

    if image.size != EXPECTED_SIZE:
        raise ValueError(
            f"{path} expected 600x1536, received {image.width}x{image.height}"
        )

    top = image.crop((0, 0, image.width, 1))
    bottom = image.crop((0, image.height - 1, image.width, image.height))
    difference = ImageChops.difference(top, bottom)
    edge_mean = sum(ImageStat.Stat(difference).mean) / 3
    return {"path": path, "size": image.size, "edge_mean": edge_mean}
```

- [ ] **Step 4: Run the two tests and verify they pass**

Run:

```powershell
python -m unittest tests.test_level_background_validation -v
```

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 5: Add batch validation and Pygame viewport coverage**

Extend `tools/validate_level_backgrounds.py` with:

```python
import argparse
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from background import ScrollingBackground


def validate_viewport_coverage(path):
    pygame.init()
    pygame.display.set_mode((1, 1))
    surface = pygame.image.load(path).convert()
    scroller = ScrollingBackground(surface)
    sentinel = (1, 254, 1)
    for offset in (0, 1, 899, 1534, 1535):
        target = pygame.Surface((600, 900))
        target.fill(sentinel)
        scroller.offset = offset
        scroller.draw(target)
        for x in range(target.get_width()):
            for y in range(target.get_height()):
                if target.get_at((x, y))[:3] == sentinel:
                    raise ValueError(f"{path} leaves an uncovered pixel at {offset}")
    pygame.quit()


def validate_levels(start_level, end_level, background_dir, edge_limit=3.0):
    results = []
    for level in range(start_level, end_level + 1):
        path = Path(background_dir) / f"lv{level}_background.jpg"
        result = inspect_background(path)
        if result["edge_mean"] > edge_limit:
            raise ValueError(
                f"{path} edge difference {result['edge_mean']:.3f} exceeds {edge_limit}"
            )
        validate_viewport_coverage(path)
        results.append(result)
    return results
```

Add a CLI with `--start-level`, `--end-level`, `--background-dir`, and `--edge-limit`, printing one line per validated file.

- [ ] **Step 6: Add a failing batch-range test**

Extend `tests/test_level_background_validation.py`:

```python
from tools.validate_level_backgrounds import validate_levels


def test_validate_levels_requires_every_file_in_range(self):
    with tempfile.TemporaryDirectory(dir=Path("tests")) as directory:
        background_dir = Path(directory)
        image = Image.new("RGB", (600, 1536), (5, 10, 20))
        image.save(background_dir / "lv2_background.jpg")

        with self.assertRaises(FileNotFoundError):
            validate_levels(2, 3, background_dir)
```

- [ ] **Step 7: Run all validator tests**

Run:

```powershell
python -m unittest tests.test_level_background_validation -v
```

Expected: `Ran 3 tests` and `OK`.

- [ ] **Step 8: Commit the validator**

```powershell
git add tools/validate_level_backgrounds.py tests/test_level_background_validation.py
git commit -m "Add level background asset validation"
```

### Task 2: Generate And Process Levels 2 To 5

**Files:**
- Create: `img/background/source/lv2_background_source.png`
- Create: `img/background/source/lv3_background_source.png`
- Create: `img/background/source/lv4_background_source.png`
- Create: `img/background/source/lv5_background_source.png`
- Modify: `img/background/lv2_background.jpg`
- Modify: `img/background/lv3_background.jpg`
- Modify: `img/background/lv4_background.jpg`
- Modify: `img/background/lv5_background.jpg`

- [ ] **Step 1: Generate Level 2**

Use built-in image generation:

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 2
Primary request: defensive deep space with a deep navy starfield, sparse small meteoroids, distant satellites, and subtle cyan navigation lights near the sides
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536 composition; low-to-medium detail; wide dark central combat corridor; environmental elements concentrated near the left and right edges
Lighting/mood: calm open space, deep navy with restrained cyan accents
Constraints: top and bottom 12% contain compatible sparse starfield; no large object crosses a vertical boundary; keep upper-left HUD area dark; no text, UI, logo, border, signature, or watermark
Avoid: photorealism, painterly blur, giant planets, dense asteroid fields, bright central objects
```

- [ ] **Step 2: Generate Level 3**

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 3
Primary request: blue-violet deep-space nebula with sparse space debris and tiny distant craft
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; blue and violet nebula structures along both sides; dark restrained central combat corridor
Lighting/mood: mysterious and colorful but readable, navy center with blue and violet edge glow
Constraints: top and bottom 12% have compatible sparse starfield and soft nebula texture; keep upper-left HUD area dark; no large boundary-crossing landmark; no text, UI, logo, border, signature, or watermark
Avoid: photorealism, high visual noise, bright center, giant planets
```

- [ ] **Step 3: Generate Level 4**

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 4
Primary request: outer asteroid belt with small and medium rocky bodies, sparse dust clouds, and dim reflected blue light
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; asteroids concentrated along the sides; wide open dark central flight corridor
Lighting/mood: increasingly dangerous deep space, navy and slate rock with restrained cyan highlights
Constraints: no asteroid blocks the center or crosses the top or bottom boundary; keep upper-left HUD area dark; no text, UI, logo, border, signature, or watermark
Avoid: photorealism, dense central debris, huge rocks, orange fire everywhere
```

- [ ] **Step 4: Generate Level 5**

```text
Use case: stylized-concept
Asset type: vertical pixel-art boss gameplay background for Level 5
Primary request: enemy-controlled deep space with partial outpost structures, antennas, and defensive platforms along the sides
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; exceptionally wide dark central boss arena; hostile structures only near the left and right edges
Lighting/mood: tense dark navy space with restrained violet glow and small red warning lights
Constraints: keep the central 55% open; top and bottom 12% contain compatible sparse starfield; keep upper-left HUD area dark; no text, insignia, logo, border, signature, or watermark
Avoid: photorealism, bright center, giant station, readable warning labels
```

- [ ] **Step 5: Save and process Levels 2 to 5**

Copy selected generated outputs to the source filenames above, then run:

```powershell
python tools/make_vertical_tile.py img/background/source/lv2_background_source.png img/background/lv2_background.jpg
python tools/make_vertical_tile.py img/background/source/lv3_background_source.png img/background/lv3_background.jpg
python tools/make_vertical_tile.py img/background/source/lv4_background_source.png img/background/lv4_background.jpg
python tools/make_vertical_tile.py img/background/source/lv5_background_source.png img/background/lv5_background.jpg
```

- [ ] **Step 6: Validate Levels 2 to 5**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 2 --end-level 5
```

Expected: four validated files, each `600x1536`, edge mean at or below `3.0`, and no uncovered viewport pixels.

- [ ] **Step 7: Create and inspect join previews**

For each image, create a `600x600` preview containing the bottom 300 rows above the top 300 rows. Reject any image with a horizontal brightness band, broken asteroid, interrupted structure, or obvious duplicated landmark.

- [ ] **Step 8: Commit Levels 2 to 5**

```powershell
git add img/background/source/lv2_background_source.png img/background/source/lv3_background_source.png img/background/source/lv4_background_source.png img/background/source/lv5_background_source.png img/background/lv2_background.jpg img/background/lv3_background.jpg img/background/lv4_background.jpg img/background/lv5_background.jpg
git commit -m "Add seamless space backgrounds for levels 2 to 5"
```

### Task 3: Generate And Process Levels 6 And 7

**Files:**
- Create: `img/background/source/lv6_background_source.png`
- Create: `img/background/source/lv7_background_source.png`
- Modify: `img/background/lv6_background.jpg`
- Modify: `img/background/lv7_background.jpg`

- [ ] **Step 1: Generate Level 6**

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 6
Primary request: high-altitude flight above Earth at dusk with subtle atmospheric glow and cloud formations near the sides
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; aerial downward-looking view; muted curved atmospheric light and clouds along the sides; dark open central flight corridor
Lighting/mood: transition from space to Earth, navy upper sky, muted cyan atmosphere, restrained warm dusk accents
Constraints: no giant full Earth disk or dominant horizontal horizon; top and bottom regions have compatible clouds and atmospheric color; keep upper-left HUD dark; no text, UI, logo, border, signature, or watermark
Avoid: side-view landscape, photorealism, bright white clouds filling the center
```

- [ ] **Step 2: Generate Level 7**

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background for Level 7
Primary request: atmospheric entry through a blue-violet upper atmosphere with long cloud formations and subtle speed streaks
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; aerial downward-looking view; cloud bands flow vertically along both sides; dark central flight corridor
Lighting/mood: energetic blue-violet atmospheric descent at late dusk
Constraints: top and bottom regions have compatible vertical cloud flow; keep upper-left HUD dark; no horizontal horizon, text, UI, logo, border, signature, or watermark
Avoid: photorealism, side-view clouds, lightning in the center, dense bright fog
```

- [ ] **Step 3: Save and process Levels 6 and 7**

```powershell
python tools/make_vertical_tile.py img/background/source/lv6_background_source.png img/background/lv6_background.jpg
python tools/make_vertical_tile.py img/background/source/lv7_background_source.png img/background/lv7_background.jpg
```

- [ ] **Step 4: Validate Levels 6 and 7**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 6 --end-level 7
```

Expected: two validated files with no uncovered viewport pixels.

- [ ] **Step 5: Inspect join previews and commit**

Reject horizontal horizons, visibly cut cloud bands, or abrupt atmosphere color changes at the join.

```powershell
git add img/background/source/lv6_background_source.png img/background/source/lv7_background_source.png img/background/lv6_background.jpg img/background/lv7_background.jpg
git commit -m "Add seamless Earth atmosphere backgrounds for levels 6 and 7"
```

### Task 4: Generate And Process Levels 8 To 10

**Files:**
- Create: `img/background/source/lv8_background_source.png`
- Create: `img/background/source/lv9_background_source.png`
- Create: `img/background/source/lv10_background_source.png`
- Modify: `img/background/lv8_background.jpg`
- Modify: `img/background/lv9_background.jpg`
- Modify: `img/background/lv10_background.jpg`

- [ ] **Step 1: Generate Level 8**

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down gameplay background for Level 8
Primary request: snow-covered mountain valley at dusk viewed directly from above
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; top-down terrain map; snow ridges and rocky cliffs along both sides; dark valley forms the central combat corridor
Lighting/mood: cold blue snow shadows with restrained warm dusk highlights
Constraints: maintain a direct top-down aerial perspective; top and bottom terrain contours must be compatible for vertical looping; keep upper-left HUD readable; no text, roads with markings, UI, logo, border, signature, or watermark
Avoid: horizon, side-view mountains, photorealism, bright snow covering the center
```

- [ ] **Step 2: Generate Level 9**

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down gameplay background for Level 9
Primary request: futuristic city at night viewed directly from above
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; top-down city blocks, rooftops, roads, and streetlights concentrated along both sides; dark central avenue, river, or park corridor
Lighting/mood: deep navy city with cyan, amber, and restrained magenta lights
Constraints: maintain a direct top-down aerial perspective; top and bottom street patterns remain compatible; keep central corridor and upper-left HUD dark; no readable signs, road text, logos, border, signature, or watermark
Avoid: isometric perspective, side-view skyline, photorealism, dense lights in the center
```

- [ ] **Step 3: Generate Level 10**

```text
Use case: stylized-concept
Asset type: vertical pixel-art top-down boss gameplay background for Level 10
Primary request: fortified military airbase at night viewed directly from above
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with small 2D pixel-art spacecraft
Composition/framing: tall portrait 600:1536; top-down hangars, radar equipment, defensive structures, parked vehicles, and runway lights concentrated along both sides; exceptionally wide dark central runway boss arena
Lighting/mood: tense deep blue-gray base with restrained cyan and red warning lights
Constraints: keep central 55% open; top and bottom runway or terrain pattern must be compatible for vertical looping; keep upper-left HUD dark; no national flags, insignia, readable labels, real-world branding, text, border, signature, or watermark
Avoid: isometric perspective, side-view buildings, photorealism, bright center, giant aircraft blocking gameplay
```

- [ ] **Step 4: Save and process Levels 8 to 10**

```powershell
python tools/make_vertical_tile.py img/background/source/lv8_background_source.png img/background/lv8_background.jpg
python tools/make_vertical_tile.py img/background/source/lv9_background_source.png img/background/lv9_background.jpg
python tools/make_vertical_tile.py img/background/source/lv10_background_source.png img/background/lv10_background.jpg
```

- [ ] **Step 5: Validate Levels 8 to 10**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 8 --end-level 10
```

Expected: three validated files with no uncovered viewport pixels.

- [ ] **Step 6: Inspect perspective, readability, and joins**

Reject any image that:

- Uses an isometric or horizon-based view.
- Places bright snow, city lights, or runway lights through the center.
- Shows a horizontal terrain or building cut at the join.
- Includes readable text, signs, flags, or insignia.

- [ ] **Step 7: Commit Levels 8 to 10**

```powershell
git add img/background/source/lv8_background_source.png img/background/source/lv9_background_source.png img/background/source/lv10_background_source.png img/background/lv8_background.jpg img/background/lv9_background.jpg img/background/lv10_background.jpg
git commit -m "Add seamless terrestrial backgrounds for levels 8 to 10"
```

### Task 5: Final Validation

**Files:**
- Verify: `img/background/lv2_background.jpg` through `img/background/lv10_background.jpg`
- Verify: `img/background/source/lv2_background_source.png` through `lv10_background_source.png`

- [ ] **Step 1: Run all unit tests**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass without warnings.

- [ ] **Step 2: Validate all nine runtime assets**

Run:

```powershell
python tools/validate_level_backgrounds.py --start-level 2 --end-level 10
```

Expected: nine successful validations.

- [ ] **Step 3: Compile actual Python files**

Run:

```powershell
python -m py_compile background.py main.py tools/__init__.py tools/make_vertical_tile.py tools/validate_level_backgrounds.py tests/__init__.py tests/test_background.py tests/test_vertical_tile.py tests/test_level_background_validation.py
```

Expected: exit code `0`.

- [ ] **Step 4: Run a dummy SDL startup smoke test**

Initialize Pygame with dummy video and audio drivers, bypass opening delays, post a `QUIT` event, and execute `main.py`.

Expected output:

```text
main startup smoke OK
```

- [ ] **Step 5: Create gameplay previews**

For each Level 2 through Level 10 background:

- Draw the background at a representative offset on a `600x900` Pygame surface.
- Add the HUD and player ship.
- Save a temporary preview under `verification/backgrounds/`.
- Inspect the sequence side by side for distinctness, progression, center readability, and correct top-down perspective on Levels 8 through 10.

- [ ] **Step 6: Remove verification previews and review Git state**

Run:

```powershell
git status --short
git diff --check
```

Expected: only intended validator, tests, source PNGs, runtime JPEGs, and this plan are changed; the existing `README.md` modification remains untouched.
