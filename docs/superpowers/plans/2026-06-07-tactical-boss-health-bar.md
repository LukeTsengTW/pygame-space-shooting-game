# Tactical Boss Health Bar Implementation Plan

## Goal
Replace the per-sprite Boss health bars with one top-mounted tactical Boss bar that matches the redesigned HUD, shows the approved Boss names, and communicates HP percentage clearly.

## Steps
1. Add focused tests for Boss name mapping, HP ratio clamping, delayed damage trail state, color thresholds, geometry, and rendering.
2. Implement `boss_health.py` for Boss display names and reusable health display state.
3. Extend `ui.py` with top Boss bar geometry, color selection, and tactical rendering.
4. Update `main.py` to draw the active Boss bar after the gameplay HUD and remove the old local Boss bars.
5. Run focused tests, compile checks, and whitespace checks.

## Boss Names
- Level 5: `VOID CRUISER`
- Level 10: `EARTH DESTROYER`
- Level 15: `ANOTHER EARTHLING`

## Acceptance Checks
- Only one fixed top Boss bar appears while a Boss is alive.
- Boss HP is clamped to `0%` through `100%`.
- The delayed damage trail never leads the real HP value after healing or Boss swaps.
- The old red/green per-sprite Boss bars no longer render.
