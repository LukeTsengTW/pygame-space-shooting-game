# Level 11 To 15 Pixel Backgrounds Design

## Goal

Replace the existing Level 11 through Level 15 backgrounds with five independently generated, vertically seamless pixel-art scenes.

The sequence uses a gradual ascent:

1. Traverse the Moon.
2. Traverse Mercury.
3. Traverse Mars.
4. Enter Jupiter's upper cloud layers.
5. Enter a galactic-core corridor for the Level 15 boss battle.

## Shared Visual Rules

- Match the approved modern pixel-art style used by Levels 1 through 10.
- Use crisp, deliberate pixel clusters rather than photorealistic or painterly rendering.
- Keep environmental density low to medium.
- Concentrate brighter terrain, clouds, stars, and landmarks toward the sides.
- Preserve a dark central combat corridor.
- Keep the upper-left HUD area relatively dark.
- Do not include text, logos, borders, signatures, watermarks, flags, or interface elements.
- Keep the top and bottom regions compatible in texture, brightness, color, and object density.
- Do not place a large crater, canyon, cloud vortex, or star cluster across a vertical boundary.

## Level Designs

### Level 11: Moon Surface

- Strict top-down aerial view of the Moon.
- Gray cratered terrain, fractured regolith, boulders, and shadowed ridges concentrated along the sides.
- A darker lunar valley or relatively smooth regolith plain forms the central combat corridor.
- Cold neutral gray palette with restrained blue-black shadows and pale silver highlights.
- Avoid flags, landers, footprints, bases, or recognizable mission equipment.

### Level 12: Mercury Surface

- Strict top-down aerial view of Mercury.
- Dense but controlled crater fields, heat-darkened rock, ridges, and fractured plains near the sides.
- Gray-brown stone with restrained gold-white sunlight and deep black shadows.
- The center remains smoother and darker than the edges.
- The level must be distinct from the Moon through warmer color, harsher contrast, and more heat-scorched terrain.

### Level 13: Mars Surface

- Strict top-down aerial view of Mars.
- Red-orange canyons, eroded ridges, dark basalt, scattered rocks, and light dust patterns near the sides.
- A dark canyon floor or wind-cleared corridor forms the central combat area.
- Use muted rust, ochre, dark red, and violet-brown shadows.
- Avoid bases, roads, vehicles, readable markings, or a visible horizon.

### Level 14: Jupiter Upper Clouds

- Strict downward view into Jupiter's upper cloud layers.
- Orange, cream, tan, and muted brown cloud bands flow vertically along both sides.
- Small and medium vortices may appear near the edges.
- A darker, calmer atmospheric channel remains in the center.
- Do not use the Great Red Spot or one dominant storm.
- Avoid horizontal bands that reveal the vertical tile join.
- Cloud motion and texture should feel continuous from top to bottom.

### Level 15: Galactic Core Boss Corridor

- Deep-space galactic-core passage with bright stellar clouds and dense star fields concentrated along the sides.
- The central 55% remains dark and open for the final boss.
- Use deep navy and black in the center, with gold-white, cyan, violet, and restrained magenta stellar light at the edges.
- No visible full spiral-galaxy shape.
- No singular black hole, giant star, or dominant circular landmark.
- The scene should be the most dramatic of Levels 11 through 15 without reducing projectile or boss readability.

## Progression

- Level 11 begins with cold, quiet lunar terrain.
- Level 12 becomes warmer and harsher on Mercury.
- Level 13 introduces richer red terrain and canyon structures on Mars.
- Level 14 transitions from solid terrain into turbulent gas-giant clouds.
- Level 15 leaves planetary environments and enters a luminous galactic-core corridor.

Each level must be visually distinct while retaining the same central gameplay layout.

## Generation And Processing

Each level is generated independently.

For every level:

1. Generate a tall source PNG with the approved level-specific prompt.
2. Save it as `img/background/source/lvN_background_source.png`.
3. Process it with `tools/make_vertical_tile.py`.
4. Export the runtime asset as `img/background/lvN_background.jpg`.
5. Validate it with `tools/validate_level_backgrounds.py`.
6. Inspect a bottom-to-top join preview.
7. Reject and regenerate sources with incorrect perspective, visible horizons, accidental text, central clutter, or landmarks that cannot loop naturally.

## Validation

Every runtime image must:

- Measure exactly `600x1536`.
- Keep average JPEG top-to-bottom edge difference at or below `3.0`.
- Cover a `600x900` Pygame viewport at all tested scroll offsets without uncovered pixels.
- Show no visible horizontal line, brightness band, or broken landmark at the join.
- Keep the player, enemies, projectiles, pickups, and HUD readable.
- Remain visually plausible through at least two complete downward loops.

Level 15 receives additional validation:

- The central 55% remains open.
- Bright stars and galactic clouds do not resemble projectiles strongly enough to cause confusion.
- The Boss 3 silhouette and health bar remain readable.

## Scope

This phase modifies only:

- `img/background/lv11_background.jpg` through `lv15_background.jpg`
- `img/background/source/lv11_background_source.png` through `lv15_background_source.png`
- Background processing or validation tests only when needed

It does not modify:

- `main.py`
- Gameplay mechanics
- Enemy or boss behavior
- Levels 1 through 10
- Levels 16 through 20
- Menu, settings, or upgrade backgrounds
