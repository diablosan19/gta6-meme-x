#!/usr/bin/env python3
"""Meme v3 for gta6-meme-x-01: a fake X thread. Rockstar announces another
GTA VI delay; the make.fun ghost replies that its agents already got paid.
The ghost appears as the reply avatar AND large at the bottom with cash."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1280
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fb(sz): return ImageFont.truetype(FONT, sz)
def fr(sz): return ImageFont.truetype(FONT_R, sz)

# Vice City gradient backdrop
stops = [(0.0, (38, 10, 82)), (0.35, (110, 30, 130)), (0.62, (219, 39, 119)),
         (0.82, (249, 115, 22)), (1.0, (253, 186, 60))]
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / H
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            col = tuple(int(c0[j] + (c1[j] - c0[j]) * f) for j in range(3))
            break
    for x in range(W):
        px[x, y] = col
img = img.convert("RGBA")
d = ImageDraw.Draw(img, "RGBA")

def card(x0, y0, x1, y1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(10, 10, 16, 242),
                        outline=(90, 90, 110, 255), width=3)

def verified(cx, cy, r=17):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(29, 155, 240))
    d.line([(cx - 8, cy), (cx - 2, cy + 7), (cx + 9, cy - 7)], fill=(255, 255, 255), width=4)

def circle_avatar(x, y, size, rgb):
    d.ellipse([x, y, x + size, y + size], fill=rgb)

# ---- Card 1: Rockstar tweet ----
card(70, 60, 1210, 470)
circle_avatar(110, 100, 96, (20, 20, 20))
d.text((158, 148), "R", font=fb(64), fill=(250, 170, 60), anchor="mm")
d.text((230, 108), "Rockstar Games", font=fb(44), fill=(255, 255, 255), anchor="la")
verified(628, 128)
d.text((230, 162), "@RockstarGames · 2h", font=fr(36), fill=(140, 150, 160), anchor="la")
d.text((110, 250), "Grand Theft Auto VI will now", font=fr(47), fill=(255, 255, 255), anchor="la")
d.text((110, 312), "release in 2027.", font=fr(47), fill=(255, 255, 255), anchor="la")
d.text((110, 388), "We appreciate your patience.", font=fr(40), fill=(200, 205, 215), anchor="la")

# ---- Card 2: make.fun reply ----
card(70, 510, 1210, 940)
ghost = Image.open(os.path.join(HERE, "ghost.png")).convert("RGBA")
av = ghost.resize((96, int(96 * ghost.height / ghost.width)), Image.LANCZOS)
img.paste(av, (110, 550), av)
d = ImageDraw.Draw(img, "RGBA")
d.text((230, 558), "make.fun", font=fb(44), fill=(255, 255, 255), anchor="la")
verified(468, 578)
d.text((230, 612), "@makefunai · 1h", font=fr(36), fill=(140, 150, 160), anchor="la")
d.text((110, 700), "our AI agents already got paid.", font=fb(50), fill=(255, 255, 255), anchor="la")
d.text((110, 768), "twice. in real money.", font=fb(50), fill=(120, 255, 170), anchor="la")
d.text((110, 852), "they never wait for release dates.", font=fr(38), fill=(200, 205, 215), anchor="la")

# ---- Bottom: big ghost with cash + caption ----
big = ghost.resize((int(ghost.width * 250 / ghost.height), 250), Image.LANCZOS)
img.paste(big, (W - big.width - 60, 990), big)
d = ImageDraw.Draw(img, "RGBA")
for i, (cx, cy, ang) in enumerate([(880, 1150, -12), (972, 1164, 3), (1058, 1148, 15)]):
    bill = Image.new("RGBA", (180, 92), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rounded_rectangle([3, 3, 177, 89], radius=10, fill=(34, 160, 60, 255),
                         outline=(190, 255, 200, 255), width=4)
    bd.text((90, 46), "$", font=fb(50), fill=(230, 255, 235), anchor="mm")
    bill = bill.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(bill, (cx, cy), bill)
d = ImageDraw.Draw(img, "RGBA")
d.text((70, 1010), "ROCKSTAR DELAYS.", font=fb(72), fill=(255, 255, 255), anchor="la",
       stroke_width=5, stroke_fill=(0, 0, 0))
d.text((70, 1100), "AGENTS GET PAID.", font=fb(72), fill=(255, 230, 90), anchor="la",
       stroke_width=5, stroke_fill=(0, 0, 0))

img.convert("RGB").save(os.path.join(HERE, "meme3.png"))
print("saved meme3.png", img.size)
