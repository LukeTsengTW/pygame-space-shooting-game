# Seamless Pixel Backgrounds Design

## Goal

Replace the current menu and gameplay backgrounds with cohesive, polished pixel-art space scenes that support continuous vertical scrolling without a visible seam.

The first delivery is a style-validation sample:

- Main menu background
- Level 1 gameplay background

The remaining backgrounds will be produced only after the sample style is approved.

## Visual Direction

- Detailed pixel art that matches the existing pixel-art ships and effects.
- Dark navy and space-blue base palette with controlled cyan, violet, and warm light accents.
- No text, logos, interface elements, borders, or watermarks inside the images.
- Low-to-medium environmental detail in gameplay backgrounds.
- The central gameplay corridor remains darker and quieter than the sides so enemies, bullets, pickups, and the player remain readable.
- Large landmarks must not cross the vertical tile boundary unless they can repeat naturally.

## Sample Assets

### Main Menu

- Scene: deep-space fleet base or orbital spaceport.
- Mood: calm, heroic, and slightly mysterious.
- Composition: environmental structures and light accents near the edges; a dark central region behind the menu title and buttons.
- Motion compatibility: the scene must remain visually plausible while scrolling downward.

### Level 1

- Scene: near-Earth orbit at the beginning of the campaign.
- Mood: clear, adventurous, and less threatening than later themes.
- Composition: sparse stars, small orbital debris, and subtle blue planetary light concentrated away from the central combat corridor.
- The scene must not include a single large planet or horizon whose repeated appearance makes the loop obvious.

## Full Background Progression

The 20 gameplay levels will use four coherent five-level themes:

1. Levels 1-5: Earth orbit and nearby defensive space.
2. Levels 6-10: colorful deep-space nebula territory.
3. Levels 11-15: asteroid belt and damaged industrial frontier.
4. Levels 16-20: hostile enemy-controlled deep space.

Each level receives its own variation, while levels in the same group share palette, motifs, and visual progression.

The final asset scope is:

- 20 gameplay backgrounds
- Main menu background
- Settings background
- Upgrade background

## Dimensions And Format

- Runtime dimensions: exactly `600x1536`.
- Final format: optimized JPEG unless seam correction produces visible JPEG edge artifacts; PNG may be used when necessary.
- Existing filenames remain unchanged when final assets replace the current files.
- Source or intermediate generated images are stored separately and are not loaded by the game.

## Seamless Processing

AI generation alone is not considered sufficient proof of seamlessness.

Each generated image will go through a deterministic vertical tiling pass:

1. Move the original top and bottom boundary into the center using a half-height wrap.
2. Repair or blend the new center boundary.
3. Keep the outer top and bottom rows identical in color and structure.
4. Tile the result vertically in a test image and inspect every join.
5. Reject or revise any image with broken objects, abrupt brightness changes, repeated landmark discontinuities, or a visible line.

Horizontal tiling is not required because the game does not scroll horizontally.

## Runtime Scrolling

The current two-rectangle background movement will be replaced with a single modulo-based vertical offset used to draw two copies of the active image.

This avoids:

- Rectangle positions drifting apart over time.
- One-pixel gaps caused by independent repositioning.
- Incorrect spacing when the active level background changes.

The same drawing helper will be used by the main menu, settings screen, upgrade screen, and gameplay.

## Validation

The sample is accepted when:

- Both images are exactly `600x1536`.
- The image top and bottom tile without a visible line at 1x scale.
- A two-copy scrolling preview remains seamless for multiple complete loops.
- Main-menu text and buttons remain legible.
- Level 1 enemies, bullets, items, HUD text, and player ship remain visually distinct.
- No generated text, signature, watermark, or unintended frame is present.
- The runtime shows no black strip or one-pixel gap during scrolling.

After sample approval, the same pipeline and visual rules will be applied to the remaining 21 backgrounds.
