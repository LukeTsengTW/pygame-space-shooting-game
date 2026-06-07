# HUD Safe Zone Gameplay Area Design

## Goal
Prevent the HUD and Boss health bar from covering active enemies by separating the screen into a fixed UI safe zone and a lower gameplay area.

## Screen Regions
- `HUD_HEIGHT = 52`
  - Compact top status strip for `LEVEL`, `SCORE`, `LIVES`, and `COIN`.
- `BOSS_BAR_HEIGHT = 30`
  - Thin Boss health bar below the compact HUD.
- `GAMEPLAY_TOP = HUD_HEIGHT + BOSS_BAR_HEIGHT`
  - The first Y coordinate where enemies, Bosses, players, items, and collision-sensitive gameplay entities may appear or move.

For the current `600 x 900` screen, this gives:
- `0-51`: compact HUD
- `52-81`: Boss bar
- `82-900`: gameplay area

The background still renders across the full screen so the UI safe zone keeps the same space backdrop instead of becoming a dead black band.

## HUD Layout
The current four large HUD cards will be replaced with one compact tactical status strip:

```text
LEVEL 5   SCORE 10   LIVES 10   COIN 80
```

The strip must be readable but low profile:
- Height stays within `52px`.
- Uses the existing tactical colors and font.
- Avoids large opaque card panels.
- Keeps enough contrast for quick reading during combat.

## Boss Health Bar Layout
The Boss health bar becomes a thin tactical bar below the HUD:

```text
VOID CRUISER  [================] 95%
```

Rules:
- Height stays within `30px`.
- Uses the approved Boss names:
  - `VOID CRUISER`
  - `EARTH DESTROYER`
  - `ANOTHER EARTHLING`
- Keeps HP percentage and delayed damage trail.
- Does not expand into the gameplay area in this change.

## Gameplay Area Rules
All active gameplay entities must respect `GAMEPLAY_TOP`.

### Enemies
- Regular enemies spawn with their visible body starting at or below `GAMEPLAY_TOP`.
- Enemy movement may leave the screen at the bottom and sides as before.
- Enemy cleanup rules remain based on `SCREEN_HEIGHT`.

### Bosses
- Boss entry points and path boundaries must be shifted down so Boss sprites do not enter the UI safe zone.
- Boss movement that currently checks `rect.top <= 0` uses `rect.top <= GAMEPLAY_TOP`.
- Boss horizontal bounds remain based on `0` and `SCREEN_WIDTH`.

### Player
- Player movement clamps `rect.top >= GAMEPLAY_TOP`.
- Existing left, right, and bottom clamps remain unchanged.
- Restart and next-level respawn positions remain near the bottom center.

### Bullets
- Player bullets may travel upward through the UI safe zone visually, then despawn above the screen as before.
- Enemy bullets originate from enemies that are already below `GAMEPLAY_TOP`, so they do not start inside the HUD.
- Collision behavior remains unchanged in this scope. Verification failures are handled as implementation bugs, not as new design scope.

### Items
- Dropped items originate from defeated enemies and therefore start in the gameplay area.
- Item falling and cleanup behavior remain unchanged.

## Architecture
Add shared geometry constants in `config.py`:

```python
HUD_HEIGHT = 52
BOSS_BAR_HEIGHT = 30
GAMEPLAY_TOP = HUD_HEIGHT + BOSS_BAR_HEIGHT
```

Update dependent modules to consume `GAMEPLAY_TOP` instead of hard-coded top-screen values:
- `player.py`: top movement clamp.
- `enemy.py`: enemy and Boss spawn/movement top bounds.
- `ui.py`: compact HUD geometry and thin Boss bar geometry.
- `main.py`: uses the shared constants for respawn or helper calls when gameplay-area math is required.

## Testing
Add or update tests for:
- Compact HUD and Boss bar both fit above `GAMEPLAY_TOP`.
- Player cannot move above `GAMEPLAY_TOP`.
- Regular enemies spawn at or below `GAMEPLAY_TOP`.
- Boss top-bound movement uses `GAMEPLAY_TOP` instead of `0`.
- Existing Boss health name, HP ratio, and delayed trail tests keep passing.

## Acceptance Criteria
- No enemy or Boss body can occupy the HUD safe zone during normal movement.
- Top UI total height is exactly `82px`, not the current large panel stack.
- HUD remains readable in combat.
- Boss health remains readable and does not block incoming enemies.
- Existing gameplay progression, scoring, player shooting, and item drops continue to work.
