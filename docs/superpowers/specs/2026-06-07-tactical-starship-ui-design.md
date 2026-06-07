# Tactical Starship UI Design

## Goal

Replace the current unrelated solid-color rectangles and background-floating
status text with one coherent tactical starship interface. The redesign must
improve visual hierarchy and readability without changing gameplay rules,
screen navigation, progression, controls, or the user's local level testing
value.

## Selected Direction

The approved direction is **A: Tactical Starship**.

- Deep navy translucent surfaces sit naturally over the existing space art.
- Cyan is the primary interactive and information accent.
- Warm gold is reserved for coins and upgrade costs.
- Red is reserved for destructive actions, danger, and unavailable states.
- Angled corners, thin borders, restrained glow, and compact labels create a
  military science-fiction appearance.
- Effects remain subtle so the interface does not compete with bullets,
  enemies, explosions, or detailed level backgrounds.

## Architecture

Create a focused `ui.py` module that contains presentation-only primitives and
theme constants. `main.py` remains responsible for screen loops, navigation,
game state, and click actions.

The shared UI module will provide:

- Theme colors, spacing, border widths, corner-cut dimensions, and text sizes.
- Cached font access for title, heading, body, small-label, and value roles.
- A translucent cut-corner panel renderer.
- A reusable tactical button renderer with normal, hover, primary, danger,
  locked, and disabled states.
- Reusable centered screen headings and supporting captions.
- A compact stat-card renderer for Level, Score, Lives, and Coin.
- A gameplay HUD renderer that lays out stat cards consistently.
- A dim overlay and modal panel for pause, completion, and game-over screens.
- A styled slider track, fill, and handle for the settings screen.

The helpers will accept a target `pygame.Surface` and explicit rectangles or
values. They will not read or mutate gameplay globals.

## Visual System

### Palette

- Background overlay: near-black navy with controlled transparency.
- Panel surface: dark blue-gray with enough opacity to separate text from art.
- Panel border: muted steel blue.
- Primary accent: bright cyan.
- Primary hover: lighter cyan with a restrained outer glow.
- Text: cool white for primary information and blue-gray for secondary labels.
- Coin: warm gold.
- Positive status and available upgrades: cyan, not saturated green.
- Danger and exit actions: muted red.
- Locked and disabled controls: desaturated gray-blue with lower text contrast.

### Typography

Continue using the shipped `font.ttf` asset. Establish a small type scale
instead of using the current 36-pixel font for every element:

- Screen title: largest, uppercase or title case, with extra letter spacing.
- Section heading: medium size and high contrast.
- Button label: medium-small and bold.
- Stat label: small uppercase text with letter spacing.
- Stat value: larger and brighter than the label.
- Supporting text and cost: small, muted, and visually secondary.

### Buttons

Buttons use one consistent height, border, internal padding, and angled-corner
shape. Hover state brightens the border and surface. The primary action is
cyan-emphasized; secondary actions remain dark; exit or destructive actions
use restrained red. Button hit rectangles remain standard
`pygame.Rect` values so existing input behavior stays intact.

### HUD

The gameplay HUD moves Level, Score, Lives, and Coin into compact translucent
cards across the top of the screen. Labels and values are separated by size
and color. Cards reserve stable space so changing numeric widths do not make
the interface jump.

The HUD must:

- Remain readable on all 15 current level backgrounds.
- Avoid covering the player's lower-screen combat area.
- Keep coins gold and lives clearly distinguishable without raw green text.
- Use the same stat-card design in the upgrade screen where applicable.

## Screen Coverage

### Main Menu

- Retain the scrolling menu background.
- Present a tactical title block and a centered vertical command panel.
- Use one button family for Play, Upgrade, Settings, Hard Mode, Credits, and
  Exit.
- Make Play the primary action, Exit the danger action, and other controls
  secondary.
- Add hover feedback without changing click actions.

### Level Selection

- Add a title, subtitle, and background dim layer.
- Replace the long single column with a compact 3-column grid for levels 1-15.
- Available levels use the normal/hover treatment.
- Locked levels use a visibly disabled treatment and retain current selection
  rules.
- Keep Back as a consistent secondary button at the bottom.

### Upgrade Menu

- Keep the current scrolling upgrade background.
- Put the coin balance in a gold-accent stat card.
- Render each upgrade as a larger tactical card containing name, current
  level, effect description, cost, and purchase state.
- Use cyan for affordable actions and a disabled treatment when funds are
  insufficient.
- Preserve all current costs and upgrade effects.

### Settings

- Keep the current scrolling settings background.
- Put control mode and volume inside a centered panel.
- Replace raw green/red rectangles with tactical controls.
- Give the volume slider a dark track, cyan fill, bordered handle, and numeric
  percentage.
- Preserve existing control switching and volume behavior.

### Pause, Stage Clear, Game Over, Completion, and Credits

- Use a dimmed space backdrop plus centered tactical modal rather than a bare
  black screen.
- Use the same title, supporting text, and button hierarchy.
- Convert keyboard-only Game Over and completion choices into clearly styled
  instructions while preserving current keys unless button input is added as
  a separate behavior change.
- Keep score animation and stage navigation behavior unchanged.
- Present credits in grouped rows with muted role labels and bright names.

## Interaction States

All clickable buttons must expose:

- Normal state.
- Hover state based on the current mouse position.
- Primary, secondary, danger, or locked semantic style.
- Disabled visual treatment where an action cannot run.

No animations beyond subtle hover emphasis are required. This keeps the work
focused and avoids adding timing state to every menu loop.

## Compatibility And Boundaries

- Keep the window at `600 x 900`.
- Keep existing background assets, music, sound effects, and `font.ttf`.
- Do not alter enemy balance, progression thresholds, score rules, coin
  rewards, upgrade prices, player controls, or navigation outcomes.
- Preserve the user's uncommitted `level = 15` local test setting.
- Do not add external packages or downloaded UI assets.
- The UI must render through Pygame primitives and the existing font asset.

## Verification

Automated checks will cover presentation logic that can be tested without an
interactive session:

- Theme and geometry helpers produce valid rectangles and surfaces.
- Button rendering supports normal, hover, danger, and disabled states.
- HUD layout stays within the `600 x 900` screen and does not overlap itself.
- Level-grid geometry creates 15 unique, in-bounds buttons.
- Existing unit tests continue to pass.

Manual smoke verification will cover:

- Main menu hover and click behavior.
- Level selection for unlocked and locked levels.
- Upgrade affordability and coin display.
- Settings control toggle and volume slider.
- Gameplay HUD readability over representative bright and dark backgrounds.
- Pause, stage clear, game over, completion, and credits screens.

## Acceptance Criteria

- No major menu uses unrelated saturated solid-color rectangles.
- Main menu, level selection, upgrade, settings, pause, results, and HUD share
  the same tactical visual language.
- Level, Score, Lives, and Coin remain readable against every gameplay
  background.
- Hover, primary, danger, locked, and disabled states are visually distinct.
- Existing actions and gameplay behavior remain unchanged.
- The complete automated test suite passes.
