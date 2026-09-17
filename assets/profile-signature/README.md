# Profile signature

A small typographic signature for the local profile draft. Two editing carets
reveal **Harvey**, briefly select the second contribution, and fade away. The
name is legible from the first frame and remains fully visible at the end.

- `light.gif` / `dark.gif`: 560 × 170 pixels; display at 280 × 85.
- `light-still.png` / `dark-still.png`: matching reduced-motion fallback.
- Duration: 3 seconds, one play. The GIFs contain no loop extension.
- Colors match GitHub's white and default dark backgrounds.
- Rendered from text and geometric shapes; no third-party artwork or fonts
  are included. Typography uses an installed copy of Avenir Next Demi Bold.

Regenerate with Python and Pillow:

```sh
python3 scripts/generate-profile-signature.py
```

The default font path is macOS-specific. Use `--font PATH --font-index INDEX`
to select an installed font on another system. This changes the typography.

Use the PNG files in a `<picture>` source for `prefers-reduced-motion: reduce`;
keep the `img` alternative text as `Harvey`. The surrounding introduction and
project links remain ordinary Markdown.
