# Seamless Pixel Backgrounds Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and integrate seamless pixel-art sample backgrounds for the main menu and Level 1, then replace the fragile two-rectangle scrolling logic with a tested modulo-based renderer.

**Architecture:** Image generation produces source artwork, while a deterministic post-processing script converts it into exact `600x1536` vertically tileable runtime assets. A focused `background.py` module owns background loading and modulo-based drawing so menus and gameplay use one implementation instead of repeating rectangle movement.

**Tech Stack:** Python 3.12, Pygame 2.6.1, built-in image generation, Python `unittest`, Pillow for offline image processing and seam metrics.

---

## File Structure

- Create `background.py`: background loading, scrolling offset, and two-copy drawing.
- Create `tools/make_vertical_tile.py`: crop/resize, vertical offset, seam blend, and final export.
- Create `tests/test_background.py`: behavior tests for modulo scrolling and draw positions.
- Create `tests/test_vertical_tile.py`: image size and vertical-edge continuity tests.
- Create `img/background/source/menu_background_sample.png`: generated menu source.
- Create `img/background/source/lv1_background_sample.png`: generated Level 1 source.
- Modify `img/background/menu_background.jpg`: final menu sample.
- Modify `img/background/lv1_background.jpg`: final Level 1 sample.
- Modify `main.py`: use the shared background renderer in menus and gameplay.

### Task 1: Add A Tested Background Scroller

**Files:**
- Create: `tests/test_background.py`
- Create: `background.py`

- [ ] **Step 1: Write the failing unit tests**

```python
import unittest

from background import ScrollingBackground


class FakeSurface:
    def __init__(self, height):
        self.height = height

    def get_height(self):
        return self.height


class FakeScreen:
    def __init__(self):
        self.calls = []

    def blit(self, surface, position):
        self.calls.append((surface, position))


class ScrollingBackgroundTests(unittest.TestCase):
    def test_advance_wraps_at_image_height(self):
        scroller = ScrollingBackground(FakeSurface(1536), speed=2)
        scroller.offset = 1535

        scroller.advance()

        self.assertEqual(scroller.offset, 1)

    def test_draw_places_two_images_exactly_one_height_apart(self):
        surface = FakeSurface(1536)
        screen = FakeScreen()
        scroller = ScrollingBackground(surface, speed=2)
        scroller.offset = 100

        scroller.draw(screen)

        self.assertEqual(
            screen.calls,
            [(surface, (0, -1436)), (surface, (0, 100))],
        )

```

- [ ] **Step 2: Run the tests and verify the expected import failure**

Run:

```powershell
py -3.12 -m unittest tests.test_background -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'background'`.

- [ ] **Step 3: Implement the minimal scroller**

```python
class ScrollingBackground:
    def __init__(self, surface, speed=1):
        self.surface = surface
        self.speed = speed
        self.offset = 0

    def set_surface(self, surface):
        self.surface = surface
        self.offset %= self.surface.get_height()

    def advance(self):
        self.offset = (self.offset + self.speed) % self.surface.get_height()

    def draw(self, screen):
        height = self.surface.get_height()
        screen.blit(self.surface, (0, self.offset - height))
        screen.blit(self.surface, (0, self.offset))
```

- [ ] **Step 4: Run the tests and verify all three pass**

Run:

```powershell
py -3.12 -m unittest tests.test_background -v
```

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 5: Commit the scroller**

```powershell
git add background.py tests/test_background.py
git commit -m "Add tested seamless background scroller"
```

### Task 2: Add A Deterministic Vertical Tile Processor

**Files:**
- Create: `tests/test_vertical_tile.py`
- Create: `tools/make_vertical_tile.py`

- [ ] **Step 1: Write failing image-processing tests**

```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.make_vertical_tile import make_vertical_tile


class VerticalTileTests(unittest.TestCase):
    def test_output_has_runtime_dimensions_and_matching_edges(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.png"
            output = Path(directory) / "output.png"
            image = Image.new("RGB", (768, 1536))
            for y in range(image.height):
                color = (y % 256, 20, 40)
                for x in range(image.width):
                    image.putpixel((x, y), color)
            image.save(source)

            make_vertical_tile(source, output, 600, 1536, blend_height=96)

            result = Image.open(output)
            self.assertEqual(result.size, (600, 1536))
            self.assertEqual(
                list(result.crop((0, 0, 600, 1)).getdata()),
                list(result.crop((0, 1535, 600, 1536)).getdata()),
            )
```

- [ ] **Step 2: Run the test and verify the expected import failure**

Run:

```powershell
py -3.12 -m unittest tests.test_vertical_tile -v
```

Expected: FAIL because `tools.make_vertical_tile` does not exist.

- [ ] **Step 3: Implement crop, wrap, blend, and edge locking**

Implement `make_vertical_tile(source_path, output_path, width, height, blend_height)` using Pillow:

```python
from pathlib import Path

from PIL import Image, ImageChops


def make_vertical_tile(source_path, output_path, width=600, height=1536, blend_height=96):
    image = Image.open(source_path).convert("RGB")
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    image = resized.crop((left, top, left + width, top + height))

    half = height // 2
    image = ImageChops.offset(image, 0, half)
    upper = image.crop((0, half - blend_height, width, half))
    lower = image.crop((0, half, width, half + blend_height))
    mask = Image.new("L", (width, blend_height))
    for y in range(blend_height):
        mask.paste(round(255 * y / max(1, blend_height - 1)), (0, y, width, y + 1))
    image.paste(Image.composite(lower, upper, mask), (0, half - blend_height // 2))

    first_row = image.crop((0, 0, width, 1))
    image.paste(first_row, (0, height - 1))
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
```

Add a CLI accepting `source`, `output`, `--width`, `--height`, and `--blend-height`.

- [ ] **Step 4: Run the test and verify it passes**

Run:

```powershell
py -3.12 -m unittest tests.test_vertical_tile -v
```

Expected: `Ran 1 test` and `OK`.

- [ ] **Step 5: Commit the processor**

```powershell
git add tools/make_vertical_tile.py tests/test_vertical_tile.py
git commit -m "Add vertical background tile processor"
```

### Task 3: Generate And Process The Two Sample Assets

**Files:**
- Create: `img/background/source/menu_background_sample.png`
- Create: `img/background/source/lv1_background_sample.png`
- Modify: `img/background/menu_background.jpg`
- Modify: `img/background/lv1_background.jpg`

- [ ] **Step 1: Generate the main-menu source**

Use the built-in image generator with:

```text
Use case: stylized-concept
Asset type: vertical pixel-art game menu background
Primary request: a polished deep-space fleet base and orbital spaceport for a vertical scrolling space shooter
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with 2D pixel-art spacecraft
Composition/framing: portrait 600:1536 composition; dark quiet central corridor for title and six menu buttons; structures, docking lights, distant ships, and nebula accents concentrated near the left and right edges
Lighting/mood: calm heroic deep navy space, subtle cyan and violet lights
Constraints: designed for vertical looping; top and bottom should contain only sparse continuous starfield and soft nebula texture; no large object crossing either vertical boundary; no text, UI, logo, border, signature, or watermark
Avoid: photorealism, painterly blur, dense central detail, planets at the top or bottom edge
```

- [ ] **Step 2: Generate the Level 1 source**

Use the built-in image generator with:

```text
Use case: stylized-concept
Asset type: vertical pixel-art gameplay background
Primary request: near-Earth defensive orbit at the beginning of a vertical scrolling space-shooter campaign
Style/medium: detailed modern pixel art, crisp deliberate pixel clusters, cohesive with 2D pixel-art spacecraft
Composition/framing: portrait 600:1536 composition; low-to-medium detail; dark central combat corridor; sparse stars, tiny orbital debris, distant satellites, and blue atmospheric light concentrated toward the sides
Lighting/mood: adventurous, readable, deep navy and restrained cyan
Constraints: designed for vertical looping; top and bottom should contain compatible sparse starfield; no large planet, horizon, station, or landmark that makes repetition obvious; no text, UI, logo, border, signature, or watermark
Avoid: photorealism, high visual noise, bright central objects, large boundary-crossing objects
```

- [ ] **Step 3: Copy generated files into the source directory**

Copy the selected built-in outputs to the exact source paths listed above without overwriting unrelated files.

- [ ] **Step 4: Process the runtime images**

Run:

```powershell
py -3.12 tools/make_vertical_tile.py img/background/source/menu_background_sample.png img/background/menu_background.jpg
py -3.12 tools/make_vertical_tile.py img/background/source/lv1_background_sample.png img/background/lv1_background.jpg
```

- [ ] **Step 5: Verify image dimensions and edge identity**

Run:

```powershell
py -3.12 -m unittest tests.test_vertical_tile -v
```

Then inspect a two-copy vertical composite of each image at the join. Reject images with a broken landmark or visible brightness band even when the first and last rows match numerically.

- [ ] **Step 6: Commit the sample assets**

```powershell
git add img/background/source/menu_background_sample.png img/background/source/lv1_background_sample.png img/background/menu_background.jpg img/background/lv1_background.jpg
git commit -m "Add seamless pixel background samples"
```

### Task 4: Integrate The Shared Scroller

**Files:**
- Modify: `main.py`
- Modify: `tests/test_background.py`

- [ ] **Step 1: Add a failing test for image switching**

Extend `tests/test_background.py`:

```python
def test_set_surface_preserves_scroll_phase(self):
    first = FakeSurface(1000)
    second = FakeSurface(2000)
    scroller = ScrollingBackground(first, speed=2)
    scroller.offset = 250

    scroller.set_surface(second)

    self.assertEqual(scroller.offset, 500)
```

- [ ] **Step 2: Run the test and verify the phase assertion fails**

Run:

```powershell
py -3.12 -m unittest tests.test_background -v
```

Expected: FAIL because the existing implementation preserves pixel offset rather than normalized scroll phase.

- [ ] **Step 3: Preserve normalized phase when switching surfaces**

Update `set_surface`:

```python
def set_surface(self, surface):
    old_height = self.surface.get_height()
    phase = self.offset / old_height if old_height else 0
    self.surface = surface
    self.offset = phase * self.surface.get_height()
```

- [ ] **Step 4: Run the tests and verify all pass**

Run:

```powershell
py -3.12 -m unittest tests.test_background -v
```

Expected: `Ran 3 tests` and `OK`.

- [ ] **Step 5: Replace repeated rectangle logic in `main.py`**

Import `ScrollingBackground`, create one gameplay scroller, and use a local scroller in `main_menu`, `setting`, and `upgrade_UI`. Each frame calls:

```python
scroller.advance()
scroller.draw(screen)
```

When the level changes:

```python
if gameplay_background.surface is not backgrounds[level - 1]:
    gameplay_background.set_surface(backgrounds[level - 1])
```

Remove the old `background_rect`, `background_rect_bottom`, independent movement, and repositioning blocks.

- [ ] **Step 6: Run all unit tests**

Run:

```powershell
py -3.12 -m unittest discover -s tests -v
```

Expected: all tests pass with no failures or errors.

- [ ] **Step 7: Commit runtime integration**

```powershell
git add main.py background.py tests/test_background.py
git commit -m "Use seamless modulo background scrolling"
```

### Task 5: Final Visual And Runtime Verification

**Files:**
- Verify: `img/background/menu_background.jpg`
- Verify: `img/background/lv1_background.jpg`
- Verify: `main.py`

- [ ] **Step 1: Run the complete automated test suite**

Run:

```powershell
py -3.12 -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 2: Run a syntax compilation check**

Run:

```powershell
py -3.12 -m compileall background.py main.py tools tests
```

Expected: exit code `0`.

- [ ] **Step 3: Launch the game and inspect the main menu**

Run:

```powershell
py -3.12 main.py
```

Skip or complete the opening sequence, then observe at least two full menu-background loops. Verify there is no black line, one-pixel gap, abrupt brightness band, or broken object at the join.

- [ ] **Step 4: Inspect Level 1 gameplay**

Start Level 1 and observe at least two full loops. Verify the ship, enemies, bullets, pickups, and HUD remain readable against the new background.

- [ ] **Step 5: Review the final diff**

Run:

```powershell
git status --short
git diff --check
```

Expected: only intended sample, runtime, test, and plan changes are present; the user's existing `README.md` modification remains untouched.
