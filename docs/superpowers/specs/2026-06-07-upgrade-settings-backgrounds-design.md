# Upgrade and Settings Background Design

## Goal

Replace the existing Upgrade and Settings page backgrounds with distinct
pixel-art scenes that match the game's current visual direction and loop
vertically without a visible seam.

## Visual Direction

### Upgrade

- Theme: blue-purple space technology workshop.
- Place energy conduits, machinery, illuminated panels, and structural details
  primarily along the left and right edges.
- Keep the center dark and relatively quiet so upgrade labels, costs, and
  buttons remain readable.
- Use brighter cyan, violet, and restrained magenta accents near the edges.
- Avoid characters, spacecraft, text, logos, borders, and dominant circular
  objects.

### Settings

- Theme: deep-blue spacecraft control room.
- Use restrained control panels, cables, vents, and cool-blue indicator lights
  along the side edges.
- Keep the scene calmer and less visually dense than the Upgrade page.
- Preserve a dark central area and a low-detail upper-left area for interface
  readability.
- Avoid characters, spacecraft, text, logos, borders, and bright central
  displays.

## Shared Composition

- Detailed modern pixel art that remains visually compatible with the game's
  existing sprites and regenerated backgrounds.
- Direct front-facing or abstract panel composition without a horizon or strong
  perspective convergence.
- Tall portrait source suitable for conversion to the runtime background.
- Side details frame the interface instead of competing with it.
- The top and bottom regions must have compatible color, brightness, texture,
  and structural flow so the existing vertical tiling tool can blend them.

## Asset Pipeline

Generate one independent source image for each page:

- `img/background/source/upgrade_background_source.png`
- `img/background/source/setting_background_source.png`

Process them through `tools/make_vertical_tile.py` to replace:

- `img/background/upgrade_background.jpg`
- `img/background/setting_background.jpg`

Both runtime files must be `600x1536` and continue using the existing
`ScrollingBackground` implementation in `main.py`.

## Validation

- Confirm both runtime images are `600x1536`.
- Measure the top-to-bottom edge difference with the existing background
  validation logic.
- Create join previews showing the bottom edge followed by the top edge and
  inspect them for visible horizontal seams.
- Create page previews with representative Upgrade and Settings interface text
  to verify readability.
- Run the complete unit test suite, Python compilation, and dummy SDL startup
  smoke test.
- Keep the user's uncommitted `main.py` change out of all commits.

## Acceptance Criteria

- Upgrade and Settings are immediately distinguishable by theme.
- Neither background has an obvious seam during vertical looping.
- Central interface content and the upper-left HUD area remain readable.
- No generated text, watermark, logo, spacecraft, or unrelated focal object is
  present.
- Existing navigation and scrolling behavior remain unchanged.
