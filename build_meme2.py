#!/usr/bin/env python3
"""Meme v2 for gta6-meme-x-01: 'THINGS WE GOT BEFORE GTA 6' checklist.
The joke and the make.fun sell are the same punchline: the only green check
is AI agents earning real money, next to the make.fun ghost fanning cash."""
from PIL import Image, ImageDraw, ImageFont
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1280
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz):
    return ImageFont.truetype(FONT, sz)

def gradient(w, h):
    stops = [(0.0, (38, 10, 82)), (0.35, (110, 30, 130)), (0.62, (219, 39, 119)),
             (0.82, (249, 115, 22)), (1.0, (253, 186, 60))]
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / h
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]; t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
                break
        for x in range(w):
            px[x, y] = col
    return img

def text_c(d, cx, y, s, fnt, fill=(255, 255, 255), stroke=6, sfill=(0, 0, 0)):
    d.text((cx, y), s, font=fnt, fill=fill, anchor="ma",
           stroke_width=stroke, stroke_fill=sfill)

img = gradient(W, H).convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

# neon grid floor
for i in range(14):
    y = 1060 + i * 16
    d.line([(0, y), (W, y)], fill=(255, 0, 128, 90), width=2)
for i in range(-10, 11):
    d.line([(W // 2 + i * 40, 1060), (W // 2 + i * 190, H)], fill=(255, 0, 128, 90), width=2)

# title
text_c(d, W // 2, 36, "THINGS WE GOT", font(92))
text_c(d, W // 2, 140, "BEFORE GTA 6", font(92), fill=(255, 230, 90))

def row(y, label, ok, stamp=None, highlight=False, label2=None):
    x0, x1, hh = 60, 1220, 190
    bg = (20, 8, 40, 215) if not highlight else (46, 20, 6, 225)
    border = (255, 215, 0, 255) if highlight else (255, 255, 255, 120)
    d.rounded_rectangle([x0, y, x1, y + hh], radius=26, fill=bg, outline=border,
                        width=6 if highlight else 3)
    # checkbox
    bx, by, bs = x0 + 34, y + hh // 2 - 42, 84
    d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=12,
                        outline=(255, 255, 255), width=6)
    if ok:
        d.line([(bx + 14, by + 44), (bx + 34, by + 64), (bx + 72, by + 18)],
               fill=(34, 255, 120), width=15)
    else:
        d.line([(bx + 18, by + 18), (bx + 66, by + 66)], fill=(255, 60, 60), width=14)
        d.line([(bx + 66, by + 18), (bx + 18, by + 66)], fill=(255, 60, 60), width=14)
    if label2:
        d.text((bx + bs + 30, y + hh // 2 - 34), label, font=font(50),
               fill=(255, 255, 255), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))
        d.text((bx + bs + 30, y + hh // 2 + 34), label2, font=font(50),
               fill=(255, 255, 255), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))
    else:
        d.text((bx + bs + 30, y + hh // 2), label, font=font(54 if len(label) < 26 else 46),
               fill=(255, 255, 255), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0))
    if stamp:
        sw, sh = 430, 84
        sx, sy = x1 - sw - 26, y + hh // 2 - sh // 2
        stamp_img = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp_img)
        sd.rounded_rectangle([4, 4, sw - 4, sh - 4], radius=10, outline=(255, 45, 45, 255), width=7)
        sd.text((sw // 2, sh // 2), stamp, font=font(44), fill=(255, 45, 45, 255), anchor="mm")
        stamp_img = stamp_img.rotate(8, expand=True, resample=Image.BICUBIC)
        img.paste(stamp_img, (sx, sy), stamp_img)

row(268, "GTA 6", ok=False, stamp="DELAYED AGAIN")
row(492, "FLYING CARS", ok=False)
row(716, "AI AGENTS EARNING", ok=True, highlight=True, label2="REAL MONEY")

# ghost with cash, right side of the highlighted row, big
ghost = Image.open(os.path.join(HERE, "ghost.png")).convert("RGBA")
gh = 430
ghost = ghost.resize((int(ghost.width * gh / ghost.height), gh), Image.LANCZOS)
gx, gy = W - ghost.width - 56, 660
img.paste(ghost, (gx, gy), ghost)
d = ImageDraw.Draw(img, "RGBA")
# cash bills fanned under the ghost
for i, (cx, cy, ang) in enumerate([(880, 1052, -14), (972, 1066, 4), (1058, 1050, 16)]):
    bill = Image.new("RGBA", (190, 96), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rounded_rectangle([3, 3, 187, 93], radius=10, fill=(34, 160, 60, 255),
                         outline=(190, 255, 200, 255), width=4)
    bd.text((95, 48), "$", font=font(52), fill=(230, 255, 235), anchor="mm")
    bill = bill.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(bill, (cx, cy), bill)
d = ImageDraw.Draw(img, "RGBA")
text_c(d, 400, 952, "ON make.fun", font(88), fill=(120, 255, 170))

# bottom caption
text_c(d, W // 2, 1152, "STILL NO GTA 6 THO", font(64), fill=(255, 255, 255))

img.convert("RGB").save(os.path.join(HERE, "meme2.png"))
print("saved meme2.png", img.size)
