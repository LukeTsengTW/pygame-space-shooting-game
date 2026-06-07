# Opening Animation Skip Design

## Goal

Allow the player to skip the opening animation with a deliberate two-key
sequence. The first key press shows `再次點擊任意鍵跳過`; the second key press
immediately ends the opening and enters the main menu.

## Design

`OpeningSkipState` owns the two-step interaction independently from Pygame. Its
first `press_key()` call exposes the prompt and returns `False`; its second call
marks the opening as skipped and returns `True`.

The opening renderer will replace blocking `pygame.time.wait()` calls with a
short frame loop. Every opening phase will poll events, redraw its current
frame, draw the prompt when requested, and cap the loop at 60 FPS. This applies
to story text typing, pauses between story lines, the credit fade, and the
final pauses.

Only `KEYDOWN` advances the skip interaction. Window close events retain their
existing behavior. When skipping, story sound effects and opening music stop
before control returns to `main_menu()`.

## Testing

Unit tests cover the initial state, first key press, second key press, and
additional key presses after skipping. Existing gameplay tests and Python
syntax compilation provide regression coverage for the integration.
