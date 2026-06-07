# Tactical Opening Interface Design

## Goal

Bring the opening sequence into the approved Tactical Starship visual system
while preserving its story, music, typewriter timing, two-step skip behavior,
and transition to the main menu.

## Selected Direction

The opening uses a **Tactical Communications Interface**:

- A dark moving starfield provides depth without competing with the text.
- A translucent cut-corner communications panel contains the story.
- Cyan borders, status marks, scan lines, and muted telemetry establish the
  same military science-fiction language as the menus and gameplay HUD.
- The story remains the primary focus and stays readable at `600 x 900`.

## Layout

Each story frame contains:

- A small top label: `MISSION BRIEFING`.
- A connection indicator such as `SECURE CHANNEL // EARTH COMMAND`.
- A centered tactical communications panel.
- The current story sentence inside the panel.
- A subtle animated scan line crossing the communications area.
- A bottom progress indicator derived from the current sentence index.
- The skip prompt at the bottom edge once it has been activated.

The background is generated with Pygame primitives. No new downloaded assets
or dependencies are required.

## Story Text Behavior

The existing story strings remain unchanged. Characters continue to appear
one at a time using the existing delay and text sound effect.

The renderer receives:

- Current visible text.
- Current sentence index.
- Total sentence count.
- Animation time used for star and scan-line positions.

The renderer does not mutate story state, audio state, or skip state.

## Skip Prompt

Replace the Chinese prompt:

`再次點擊任意鍵跳過`

with:

`PRESS ANY KEY AGAIN TO SKIP`

The prompt appears only after the first keyboard or mouse-button input, exactly
as it does now. The second accepted input skips the opening. Input semantics
remain unchanged.

The prompt is displayed inside a compact translucent status strip with cyan
bordering so it remains readable over the starfield.

## Creator Credit

Replace the bare `Made by LukeTseng` black-screen text with a tactical
identification card:

- Small label: `DEVELOPED BY`
- Main value: `LukeTseng`
- Supporting line: `PYGAME EDITION`
- Cyan identification border and restrained scan-line detail

The card keeps the current fade-in, hold, and fade-out sequence. Alpha affects
the complete card surface rather than only the text.

## Architecture

Add presentation helpers to `ui.py`:

- `draw_tactical_starfield(surface, tick)`
- `draw_opening_briefing(surface, text, step, total_steps, tick)`
- `draw_opening_skip_prompt(surface, prompt)`
- `create_creator_card(size)`

`main.py` continues to own:

- Opening event processing.
- Typewriter loop.
- Wait durations.
- Music and sound playback.
- Fade alpha loops.
- Returning early when skip is requested.

This keeps rendering reusable and the existing flow behavior intact.

## Compatibility And Boundaries

- Keep the existing `600 x 900` window.
- Keep all current story text, music, sound effects, and timing values.
- Keep keyboard and mouse-button skip inputs.
- Do not change the first-input-to-reveal and second-input-to-skip behavior.
- Do not alter main-menu startup or gameplay state.
- Preserve the current uncommitted UI work and `level = 15` test value.

## Verification

Automated tests will verify:

- The English skip prompt constant is exact.
- Starfield rendering is deterministic for the same tick.
- Opening frames draw within a `600 x 900` surface.
- Briefing progress supports the first and final story steps.
- Creator-card rendering produces a non-empty alpha surface.
- Existing `OpeningSkipState` tests continue to pass.

Manual preview verification will inspect:

- A partially typed briefing line.
- A complete briefing line with the skip prompt visible.
- The creator identification card.
- Text readability and visual consistency with the Tactical Starship menus.

## Acceptance Criteria

- The opening no longer uses a plain black screen with isolated white text.
- The entire sequence matches the Tactical Starship interface.
- Story text remains readable and unchanged.
- The visible skip prompt is English:
  `PRESS ANY KEY AGAIN TO SKIP`.
- Existing timing, audio, skip behavior, and main-menu transition remain
  unchanged.
