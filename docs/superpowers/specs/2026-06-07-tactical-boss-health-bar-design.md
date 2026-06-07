# Tactical Boss Health Bar Design

## Goal

Replace the small Boss-following red and green bars with one fixed,
high-visibility Tactical Starship Boss health display below the gameplay HUD.
The change must improve combat readability without changing Boss health,
damage, movement, spawning, or rewards.

## Placement

The Boss bar is fixed near the top of the `600 x 900` screen:

- It sits below the existing Level, Score, Lives, and Coin HUD cards.
- It spans most of the screen width.
- It never follows Boss movement or rotation.
- It remains inside the screen when a Boss moves partially off-screen.
- It is drawn only while a living Boss is active.

## Boss Names

The display uses these exact names:

- Level 5 / `Boss_1`: `VOID CRUISER`
- Level 10 / `Boss_2`: `EARTH DESTROYER`
- Level 15 / `Boss_3`: `ANOTHER EARTHLING`

Names are mapped by Boss class rather than inferred from the current level so
the correct name remains stable during restarts or unusual test states.

## Visual Design

The display uses a wide cut-corner tactical panel consistent with `ui.py`.
It contains:

- A small `BOSS TARGET` status label.
- The Boss name in prominent uppercase text.
- Current and maximum HP with thousands separators.
- A numeric health percentage.
- A wide health track with subtle segment markers.
- A cyan border and dark translucent panel background.

The bar fill changes by current health ratio:

- Above 50%: cyan.
- From 20% through 50%: gold.
- Below 20%: red.

The ratio is always clamped to `0.0` through `1.0`, protecting the renderer
from over-healing or negative post-hit HP.

## Delayed Damage Feedback

A secondary delayed-health layer shows recently lost health:

- The immediate fill shrinks as soon as Boss HP changes.
- A muted damage-trail fill remains at the previous ratio briefly.
- The trail then moves toward the actual ratio at a controlled rate.
- Healing or Boss replacement resets the trail immediately rather than
  animating from an unrelated previous Boss.

The state stores:

- The identity of the currently tracked Boss.
- The displayed delayed ratio.
- The latest update timestamp.
- The timestamp of the most recent damage change.

This state affects presentation only and never writes to `boss.hp`.

## Architecture

Create `boss_health.py` for non-rendering Boss health behavior:

- `BOSS_NAMES`: exact class-name-to-display-name mapping.
- `get_boss_display_name(boss)`.
- `health_ratio(current, maximum)`.
- `BossHealthDisplayState`: delayed-damage state and update logic.

Add to `ui.py`:

- `boss_health_color(ratio)`.
- `boss_health_bar_rect(screen_width)`.
- `draw_boss_health_bar(surface, name, current, maximum, delayed_ratio)`.

Update `main.py`:

- Create one `BossHealthDisplayState`.
- Select the first living active Boss from the three Boss groups.
- Update and draw the fixed bar after the normal gameplay HUD.
- Remove `draw_health_bar()` and the separate Boss 3 red/green bar block.
- Reset tracking automatically when there is no active Boss.

## Rendering Order

Gameplay rendering order remains:

1. Scrolling background.
2. Bosses, enemies, projectiles, items, and player.
3. Standard gameplay HUD.
4. Fixed Boss health bar.

Drawing the Boss bar last prevents sprites and projectiles from obscuring it.

## Compatibility And Boundaries

- Keep all existing Boss `hp` and `maxhp` values.
- Keep Boss classes, directions, movement, attacks, collisions, and rewards.
- Keep the standard gameplay HUD unchanged.
- Do not add external assets or packages.
- Preserve current uncommitted user changes.

## Verification

Automated tests will verify:

- All three Boss classes map to the exact approved names.
- Health ratios clamp below zero and above maximum.
- Color thresholds select cyan, gold, and red correctly.
- The fixed bar rectangle is in bounds and below the standard HUD.
- Delayed health does not lead actual health after healing or Boss changes.
- Delayed health remains briefly after damage, then approaches actual health.
- Rendering works for full, half, critical, zero, and very large HP values.

Manual preview verification will inspect:

- `VOID CRUISER` at high health.
- `EARTH DESTROYER` at medium health with a visible damage trail.
- `ANOTHER EARTHLING` at critical health.
- Alignment below the existing HUD on a bright level background.

## Acceptance Criteria

- Boss-following red and green bars are removed.
- Boss 3 no longer has a separate duplicate health-bar path.
- A single fixed Boss display appears below the standard HUD.
- The exact approved Boss names are shown.
- Current HP, maximum HP, percentage, threshold colors, segmented styling, and
  delayed damage feedback are readable.
- Combat behavior and balance remain unchanged.
