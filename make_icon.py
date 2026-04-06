"""Generate video_editor.ico – film-strip + scissors design."""
from PIL import Image, ImageDraw
import math, os

AMBER  = (240, 165,   0)
BG     = ( 17,  17,  17)
CARD   = ( 40,  40,  40)
WHITE  = (255, 255, 255)
DARK   = ( 80,  80,  80)


def draw_icon(size):
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d    = ImageDraw.Draw(img)
    s    = size
    pad  = s * 0.06
    r    = s * 0.18          # corner radius

    # ── rounded background ──
    d.rounded_rectangle([pad, pad, s - pad, s - pad],
                        radius=r, fill=BG + (255,))

    # ── film-strip holes (top row) ──
    hole_w = s * 0.09
    hole_h = s * 0.07
    hole_r = s * 0.025
    n_holes = 5
    strip_y1 = s * 0.13
    strip_y2 = s * 0.25
    d.rectangle([pad, strip_y1, s - pad, strip_y2], fill=CARD + (255,))
    gap = (s - pad * 2 - n_holes * hole_w) / (n_holes + 1)
    for i in range(n_holes):
        hx = pad + gap + i * (hole_w + gap)
        hy = (strip_y1 + strip_y2) / 2 - hole_h / 2
        d.rounded_rectangle([hx, hy, hx + hole_w, hy + hole_h],
                            radius=hole_r, fill=BG + (255,))

    # ── film-strip holes (bottom row) ──
    strip_by1 = s * 0.75
    strip_by2 = s * 0.87
    d.rectangle([pad, strip_by1, s - pad, strip_by2], fill=CARD + (255,))
    for i in range(n_holes):
        hx = pad + gap + i * (hole_w + gap)
        hy = (strip_by1 + strip_by2) / 2 - hole_h / 2
        d.rounded_rectangle([hx, hy, hx + hole_w, hy + hole_h],
                            radius=hole_r, fill=BG + (255,))

    # ── amber scissors in the centre ──
    cx, cy = s / 2, s / 2 + s * 0.03
    bl     = s * 0.24   # blade length
    bw     = s * 0.055  # blade width
    pivot  = s * 0.06   # handle radius
    ang    = 28         # opening angle in degrees

    for sign in (+1, -1):
        a = math.radians(sign * ang)
        # blade
        tip_x = cx + bl * math.cos(a)
        tip_y = cy - bl * math.sin(a)
        perp_x = -math.sin(a) * bw * 0.5
        perp_y = -math.cos(a) * bw * 0.5
        blade = [
            (cx + perp_x, cy + perp_y),
            (cx - perp_x, cy - perp_y),
            (tip_x - perp_x * 0.2, tip_y - perp_y * 0.2),
            (tip_x + perp_x * 0.2, tip_y + perp_y * 0.2),
        ]
        d.polygon(blade, fill=AMBER + (255,))

        # handle ring
        hr = pivot
        hx = cx - hr * 1.15 * math.cos(a)
        hy = cy + hr * 1.15 * math.sin(a)
        d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr],
                  outline=AMBER + (255,), width=max(2, int(s * 0.04)))

    # ── tiny amber cut-line (vertical) ──
    lx = cx + s * 0.01
    d.line([(lx, s * 0.27), (lx, s * 0.74)],
           fill=AMBER + (160,), width=max(1, int(s * 0.018)))

    return img


sizes = [16, 32,48, 64, 128, 256]
frames = [draw_icon(sz) for sz in sizes]

out = os.path.join(os.path.dirname(__file__), "video_editor.ico")
frames[-1].save(out, format="ICO", sizes=[(sz, sz) for sz in sizes],
                append_images=frames[:-1])
print(f"Icon saved to {out}")
