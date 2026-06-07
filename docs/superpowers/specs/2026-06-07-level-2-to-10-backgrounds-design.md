# Level 2 To 10 Pixel Backgrounds Design

## Goal

Replace the existing Level 2 through Level 10 backgrounds with nine independently generated, vertically seamless pixel-art scenes.

This phase extends the approved Level 1 visual direction:

- Detailed modern pixel art.
- Low-to-medium environmental density.
- A dark, readable central combat corridor.
- Environmental landmarks and brighter details concentrated toward the sides.
- Exact `600x1536` runtime dimensions.

This specification replaces the earlier proposal that Levels 6 through 10 use a deep-space nebula theme.

## Shared Visual Rules

- Match the existing pixel-art ships, projectiles, enemies, and Level 1 background.
- Use deliberate pixel clusters rather than photorealistic or painterly rendering.
- Keep the center darker and quieter than the edges.
- Do not include text, logos, borders, signatures, watermarks, or interface elements.
- Do not place a large landmark across the top or bottom boundary.
- Keep the top and bottom regions compatible in color, brightness, and visual density.
- Avoid bright flashes or dense texture behind the HUD area in the upper-left corner.

## Level Progression

### Level 2: Defensive Deep Space

- Deep navy starfield.
- Sparse small meteoroids and distant satellites.
- Subtle cyan navigation lights near the edges.
- Calm and open composition with slightly more activity than Level 1.

### Level 3: Blue-Violet Nebula

- Blue and violet nebula structures concentrated along both sides.
- Sparse space debris and tiny distant craft.
- Dark central corridor with restrained star density.
- More colorful than Level 2 without becoming visually noisy.

### Level 4: Outer Asteroid Belt

- Small and medium rocky bodies concentrated along the sides.
- Sparse dust clouds and dim reflected blue light.
- No large asteroid may block the central corridor or cross a vertical boundary.
- The scene should feel more dangerous than Levels 2 and 3.

### Level 5: Enemy Deep-Space Outpost

- Dark enemy-controlled space.
- Partial outpost structures, antennas, or defensive platforms along the sides.
- Restrained red warning lights mixed with deep blue and violet space.
- The center remains open for the first boss encounter.

### Level 6: Above Earth At Dusk

- High-altitude view above Earth during dusk.
- Subtle curved atmospheric glow and cloud formations near the sides.
- Navy upper sky transitioning into muted cyan and warm dusk tones.
- Do not show a giant full Earth disk or a dominant horizon across the screen.

### Level 7: Atmospheric Entry

- Blue-violet upper atmosphere viewed from above.
- Long cloud formations and atmospheric streaks flow vertically along the sides.
- The central flight corridor remains dark enough for combat readability.
- The scene transitions naturally from Level 6 toward the terrestrial stages.

### Level 8: Snow Mountain Valley At Dusk

- Vertical top-down aerial view.
- Snow-covered mountain ridges and cliffs along the sides.
- A dark valley or canyon forms the central combat corridor.
- Cool blue snow shadows with restrained warm dusk light.
- Avoid a realistic perspective horizon; the terrain must scroll as a top-down map.

### Level 9: City At Night

- Vertical top-down aerial view of a futuristic city.
- Buildings, blocks, roads, and streetlights concentrated near the sides.
- A dark central avenue, river, park, or open urban corridor supports combat.
- Deep navy structures with cyan, amber, and restrained magenta lights.
- Avoid readable signs, text, traffic markings, or unique landmarks that expose repetition.

### Level 10: Military Base At Night

- Vertical top-down aerial view of a fortified military airbase.
- Hangars, defensive structures, parked vehicles, radar equipment, and runway lights near the sides.
- A dark runway or central launch corridor remains open for the boss fight.
- Deep blue-gray materials with cyan and red warning lights.
- No national flags, insignia, readable labels, or real-world military branding.

## Time And Color Progression

The visual sequence moves from space toward Earth:

1. Levels 2-5: deep navy space with increasing violet and hostile red accents.
2. Level 6: dusk above Earth.
3. Level 7: blue-violet atmospheric entry.
4. Level 8: dusk snow mountains.
5. Levels 9-10: night city and night military base.

The sequence should feel continuous while every level remains visually distinct.

## Generation And Processing

Each level is generated independently rather than derived from a shared base image.

For every level:

1. Generate a tall source PNG using the approved style and level-specific composition.
2. Save the source as `img/background/source/lvN_background_source.png`.
3. Process it through `tools/make_vertical_tile.py`.
4. Export the runtime image to `img/background/lvN_background.jpg`.
5. Generate a two-copy join preview for visual inspection.
6. Reject and regenerate any source with illegible central composition, accidental text, unsuitable perspective, or landmarks that cannot tile naturally.

## Seam Validation

Every runtime image must:

- Measure exactly `600x1536`.
- Cover a `600x900` Pygame surface at all tested offsets without uncovered pixels.
- Show no horizontal black line, brightness band, or broken object at the vertical join.
- Keep top and bottom edge color difference below a visually detectable level after JPEG encoding.
- Remain visually plausible for at least two complete downward loops.

## Gameplay Readability

Visual inspection must confirm:

- The player ship remains visible near the lower center.
- Enemies and projectiles remain distinct in the central corridor.
- The upper-left HUD remains readable.
- Boss stages at Levels 5 and 10 provide a particularly open center.
- Snow, city lights, runway lights, stars, and debris do not resemble projectiles or pickups strongly enough to cause confusion.

## Scope

This phase modifies only:

- `lv2_background.jpg` through `lv10_background.jpg`
- Their corresponding source PNG files
- Validation utilities or tests needed to verify the nine assets

It does not modify Level 1, Levels 11-20, menu backgrounds, gameplay mechanics, or UI layout.
