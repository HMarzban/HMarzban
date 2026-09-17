#!/usr/bin/env python3
"""Render the profile's small, single-play collaborative editing signature.

Requires Pillow. Pass --font and --font-index to use another installed font.
No font files, remote assets, or network requests are bundled in the output.
"""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-signature"
SIZE = (560, 170)
SCALE = 2
TEXT = "Harvey"
FRAMES = 60
FRAME_MS = 50
THEMES = {
    "light": {"background": "#ffffff", "ink": "#1f2328", "coral": "#ba624f", "sage": "#638268"},
    "dark": {"background": "#0d1117", "ink": "#f0f6fc", "coral": "#dc907d", "sage": "#9bb39e"},
}


def smooth(start, end, t):
    progress = max(0.0, min(1.0, (t - start) / (end - start)))
    return progress * progress * (3.0 - 2.0 * progress)


def rgb(hex_color):
    return tuple(bytes.fromhex(hex_color.lstrip("#")))


def render(theme, font, t):
    canvas = Image.new("RGB", tuple(v * SCALE for v in SIZE), theme["background"])
    layer = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(layer)
    x, baseline = 12 * SCALE, 122 * SCALE
    split = x + round(font.getlength("Har"))
    end = x + round(font.getlength(TEXT))
    top, bottom = 33 * SCALE, 146 * SCALE

    def rect(bounds, color, opacity):
        if opacity > 0:
            draw.rectangle(tuple(round(v) for v in bounds), fill=rgb(color) + (round(255 * opacity),))

    # The first editor reveals "Har"; the second completes "vey".
    first = x + (split - x) * smooth(0.10, 0.70, t)
    second = split + (end - split) * smooth(0.48, 1.08, t)
    # A brief selection on the second contribution, with no fake UI around it.
    selection = smooth(1.12, 1.30, t) * (1 - smooth(1.64, 1.92, t))
    rect((split - 2 * SCALE, top, end + 2 * SCALE, bottom), theme["sage"], selection * 0.16)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), layer)

    letters = Image.new("RGBA", canvas.size)
    ImageDraw.Draw(letters).text((x, baseline), TEXT, font=font, anchor="ls", fill=theme["ink"])
    # Keep the complete name legible even when a viewer freezes the first GIF
    # frame. The cursors strengthen the ink rather than typing into blank space.
    quiet_letters = letters.copy()
    quiet_letters.putalpha(letters.getchannel("A").point(lambda alpha: round(alpha * 0.72)))
    canvas = Image.alpha_composite(canvas, quiet_letters)
    reveal = Image.new("L", canvas.size)
    reveal_draw = ImageDraw.Draw(reveal)
    reveal_draw.rectangle((x, 0, round(first), canvas.height), fill=255)
    if t >= 0.48:
        reveal_draw.rectangle((split, 0, round(second), canvas.height), fill=255)
    letters.putalpha(Image.composite(letters.getchannel("A"), Image.new("L", canvas.size), reveal))
    canvas = Image.alpha_composite(canvas, letters)

    cursors = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(cursors)

    def caret(position, color, opacity, cap_at_top):
        if opacity <= 0:
            return
        rgba = rgb(color) + (round(255 * opacity),)
        position = round(position)
        draw.rounded_rectangle((position, top - 3 * SCALE, position + 3 * SCALE, bottom + 2 * SCALE), radius=SCALE, fill=rgba)
        y = top - 7 * SCALE if cap_at_top else bottom - SCALE
        draw.rounded_rectangle((position - 2 * SCALE, y, position + 7 * SCALE, y + 8 * SCALE), radius=2 * SCALE, fill=rgba)

    caret(first + 2 * SCALE, theme["coral"], smooth(0, 0.10, t) * (1 - smooth(1.48, 1.92, t)), True)
    caret(second + 3 * SCALE, theme["sage"], smooth(0.38, 0.50, t) * (1 - smooth(2.02, 2.48, t)), False)
    canvas = Image.alpha_composite(canvas, cursors)
    return canvas.convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--font", default="/System/Library/Fonts/Avenir Next.ttc")
    parser.add_argument("--font-index", type=int, default=2, help="Default: Avenir Next Demi Bold")
    args = parser.parse_args()
    font = ImageFont.truetype(args.font, 122 * SCALE, index=args.font_index)
    OUT.mkdir(parents=True, exist_ok=True)

    for name, theme in THEMES.items():
        frames = [render(theme, font, i * FRAME_MS / 1000) for i in range(FRAMES)]
        still = render(theme, font, 3.0)
        still.save(OUT / f"{name}-still.png", optimize=True)
        # Deliberately omit the GIF loop extension. Absent means one play;
        # loop=0 would mean infinite looping, and loop=1 would repeat once.
        palette = Image.new("RGB", (SIZE[0], SIZE[1] * 4))
        for i, frame_index in enumerate((0, 12, 28, 59)):
            palette.paste(frames[frame_index], (0, i * SIZE[1]))
        palette = palette.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        # Preserve GitHub's exact background instead of allowing quantization
        # to average it with the translucent selection and create a visible box.
        exact_colors = [channel for key in ("background", "ink", "coral", "sage") for channel in rgb(theme[key])]
        colors = exact_colors + palette.getpalette()[: (256 - 4) * 3]
        for offset in range(0, len(colors), 3):
            for key, tolerance in (("background", 8), ("ink", 4)):
                exact = rgb(theme[key])
                if max(abs(a - b) for a, b in zip(colors[offset : offset + 3], exact)) <= tolerance:
                    colors[offset : offset + 3] = exact
                    break
        palette.putpalette(colors)
        indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
        indexed[0].save(OUT / f"{name}.gif", save_all=True, append_images=indexed[1:], duration=FRAME_MS, optimize=True, disposal=1)

        with Image.open(OUT / f"{name}.gif") as gif:
            assert gif.size == SIZE
            assert "loop" not in gif.info
            assert b"NETSCAPE" not in (OUT / f"{name}.gif").read_bytes()
            total = 0
            for i in range(gif.n_frames):
                gif.seek(i)
                total += gif.info["duration"]
            assert total == FRAMES * FRAME_MS, total
            assert gif.convert("RGB").getbbox()
            print(f"{name}: {gif.n_frames} frames, {total} ms, one play, {(OUT / f'{name}.gif').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
