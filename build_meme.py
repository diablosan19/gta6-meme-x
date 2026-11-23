#!/usr/bin/env python3
"""Build the gta6-meme-x-01 entry image: skeleton gamer waiting for GTA 6
vs the make.fun ghost counting cash, Vice City sunset backdrop."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = H = 1280
HORIZON = 860
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---------- sky gradient ----------
stops = [
    (0.00, (43, 16, 85)),     # deep purple
    (0.35, (123, 44, 141)),   # purple-pink
    (0.62, (215, 65, 119)),   # hot pink
    (0.82, (255, 110, 90)),   # coral
    (1.00, (255, 176, 71)),   # orange at horizon
]
ys = np.linspace(0, 1, HORIZON)
sky = np.zeros((HORIZON, W, 3), dtype=np.uint8)
for i in range(len(stops) - 1):
    y0, c0 = stops[i]
    y1, c1 = stops[i + 1]
    m = (ys >= y0) & (ys <= y1)
    t = (ys[m] - y0) / max(y1 - y0, 1e-6)
    for ch in range(3):
        sky[m, :, ch] = (c0[ch] + (c1[ch] - c0[ch]) * t)[:, None]
img = Image.new("RGB", (W, H), (26, 11, 46))
img.paste(Image.fromarray(sky), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---------- retro sun ----------
sun_cx, sun_cy, sun_r = 400, HORIZON - 60, 300
sun = Image.new("RGBA", (sun_r * 2, sun_r * 2), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
for yy in range(sun_r * 2):
    t = yy / (sun_r * 2)
    col = (255, int(214 - 110 * t), int(90 - 40 * t))
    sd.line([(0, yy), (sun_r * 2, yy)], fill=col + (255,))
mask = Image.new("L", (sun_r * 2, sun_r * 2), 0)
ImageDraw.Draw(mask).ellipse([0, 0, sun_r * 2, sun_r * 2], fill=255)
img.paste(sun, (sun_cx - sun_r, sun_cy - sun_r), mask)
d = ImageDraw.Draw(img, "RGBA")
# sun stripe cuts near the bottom of the sun
for i, yy in enumerate(range(HORIZON - 130, HORIZON, 26)):
    d.rectangle([sun_cx - sun_r, yy, sun_cx + sun_r, yy + 5 + i * 3], fill=(215, 65, 119, 255))
d.rectangle([0, HORIZON - 2, W, HORIZON + 2], fill=(0, 240, 255, 255))

# ---------- neon grid floor ----------
d.rectangle([0, HORIZON, W, H], fill=(26, 11, 46))
vp = (520, HORIZON)
for gx in range(-1600, 3201, 200):
    d.line([vp, (gx, H)], fill=(255, 46, 170, 190), width=3)
yy, gap = HORIZON + 14, 14
while yy < H:
    d.line([(0, yy), (W, yy)], fill=(0, 229, 255, 170), width=3)
    gap = int(gap * 1.45)
    yy += gap

# ---------- palm silhouettes ----------
def palm(x, y, s, flip=1):
    pts = []
    for t in np.linspace(0, 1, 24):
        pts.append((x + flip * 26 * s * t * t, y - 210 * s * t))
    d.line(pts, fill=(12, 4, 26, 255), width=max(4, int(13 * s)))
    tx, ty = pts[-1]
    for ang in (-165, -125, -85, -45, -8, 28):
        fr = []
        for t in np.linspace(0, 1, 16):
            a = math.radians(ang)
            fx = tx + flip * math.cos(a) * 120 * s * t
            fy = ty + math.sin(a) * 60 * s * t + 95 * s * t * t
            fr.append((fx, fy))
        d.line(fr, fill=(12, 4, 26, 255), width=max(3, int(8 * s)))

palm(90, HORIZON + 6, 1.05, 1)

# ---------- LEFT: skeleton gamer at a TV ----------
room = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(room)
# TV on a stand
rd.rectangle([70, 470, 430, 700], fill=(10, 10, 18, 255), outline=(0, 240, 255, 255), width=5)
rd.rectangle([88, 488, 412, 682], fill=(16, 22, 44, 255))
f_tv = ImageFont.truetype(FONT, 74)
rd.text((250, 540), "GTA VI", font=f_tv, anchor="mm", fill=(255, 210, 63, 255))
f_soon = ImageFont.truetype(FONT, 30)
rd.text((250, 610), "COMING SOON…", font=f_soon, anchor="mm", fill=(140, 220, 255, 255))
rd.rectangle([215, 700, 285, 730], fill=(10, 10, 18, 255))
rd.rectangle([140, 730, 360, 748], fill=(10, 10, 18, 255))
# wall sign
rd.rectangle([52, 300, 448, 372], fill=(20, 12, 36, 235), outline=(255, 46, 170, 255), width=4)
f_sign = ImageFont.truetype(FONT, 34)
rd.text((250, 336), "DAY 4,380 OF WAITING", font=f_sign, anchor="mm", fill=(255, 235, 160, 255))

bone = (232, 228, 210, 255)
bone_d = (190, 184, 165, 255)
# chair
rd.polygon([(520, 640), (610, 640), (640, 830), (545, 830)], fill=(24, 10, 40, 255))
rd.rectangle([520, 820, 660, 845], fill=(24, 10, 40, 255))
# skeleton: skull
rd.ellipse([468, 560, 548, 648], fill=bone)
rd.rectangle([486, 630, 530, 664], fill=bone)  # jaw
for ex in (492, 524):
    rd.ellipse([ex - 9, 592, ex + 9, 616], fill=(15, 10, 25, 255))
rd.polygon([(508, 612), (503, 628), (513, 628)], fill=(15, 10, 25, 255))
for tx_ in range(492, 524, 10):
    rd.line([(tx_, 640), (tx_, 656)], fill=(120, 114, 96, 255), width=3)
# spine + ribs
rd.line([(508, 664), (516, 790)], fill=bone, width=9)
for i, ry in enumerate(range(690, 776, 21)):
    w_ = 52 - i * 6
    rd.arc([516 - w_, ry - 14, 516 + w_, ry + 20], start=300, end=240, fill=bone_d, width=6)
# pelvis + legs (sitting, stretched toward TV)
rd.ellipse([486, 782, 534, 812], fill=bone)
rd.line([(520, 800), (430, 838)], fill=bone, width=10)
rd.line([(430, 838), (352, 828)], fill=bone, width=9)
rd.line([(528, 806), (462, 852)], fill=bone, width=10)
rd.line([(462, 852), (392, 850)], fill=bone, width=9)
# arm reaching forward holding a controller
rd.line([(514, 700), (428, 742)], fill=bone, width=9)
rd.line([(428, 742), (368, 730)], fill=bone, width=8)
rd.rounded_rectangle([316, 706, 386, 748], 16, fill=(14, 14, 22, 255), outline=(0, 240, 255, 255), width=3)
rd.ellipse([330, 718, 342, 730], fill=(255, 70, 90, 255))
rd.ellipse([356, 718, 368, 730], fill=(70, 220, 120, 255))
# long white beard hanging from the jaw (old-man gag on top of skeleton)
beard = [(492, 648), (526, 648), (534, 730), (522, 806), (508, 822), (496, 790), (488, 716)]
rd.polygon(beard, fill=(245, 245, 248, 225))
rd.ellipse([468, 560, 548, 648], outline=(200, 196, 180, 255), width=2)
# cobwebs: corner fan top-left + strands on TV/chair
web = (255, 255, 255, 110)
for r_ in (46, 92, 138, 184):
    rd.arc([-r_, -r_, r_, r_], start=0, end=90, fill=web, width=2)
for a_ in (12, 32, 52, 72):
    rd.line([(0, 0), (230 * math.cos(math.radians(a_)), 230 * math.sin(math.radians(a_)))], fill=web, width=2)
for sx, sy in ((430, 470), (610, 640), (70, 470)):
    for dx, dy in ((58, 26), (30, 52), (74, 62)):
        rd.line([(sx, sy), (sx + dx, sy + dy)], fill=web, width=2)
    rd.arc([sx + 8, sy + 6, sx + 62, sy + 52], start=20, end=160, fill=web, width=2)
img.paste(room, (0, 0), room)
d = ImageDraw.Draw(img, "RGBA")

# ---------- RIGHT: make.fun ghost counting cash ----------
ghost = Image.open("ghost.png").convert("RGBA")
GH = 560
ghost = ghost.resize((int(ghost.width * GH / ghost.height), GH), Image.LANCZOS)
gx, gy = 700, 300
img.paste(ghost, (gx, gy), ghost)
d = ImageDraw.Draw(img, "RGBA")

def bill(x, y, w_, ang, label="$"):
    b = Image.new("RGBA", (w_, int(w_ * 0.45)), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    bd.rounded_rectangle([0, 0, w_ - 1, int(w_ * 0.45) - 1], 8, fill=(46, 174, 84, 255), outline=(210, 255, 220, 255), width=4)
    bd.ellipse([w_ * 0.38, w_ * 0.08, w_ * 0.62, w_ * 0.37], outline=(210, 255, 220, 255), width=3)
    fb = ImageFont.truetype(FONT, int(w_ * 0.26))
    bd.text((w_ / 2, w_ * 0.225), label, font=fb, anchor="mm", fill=(230, 255, 238, 255))
    b = b.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(b, (int(x), int(y)), b)

def coin(x, y, r_):
    d.ellipse([x - r_, y - r_, x + r_, y + r_], fill=(255, 196, 0, 255), outline=(184, 128, 0, 255), width=4)
    fc = ImageFont.truetype(FONT, int(r_ * 1.15))
    d.text((x, y), "$", font=fc, anchor="mm", fill=(146, 96, 0, 255))

# fanned bills in front of the ghost + a pile below
bill(688, 742, 190, 18)
bill(742, 700, 200, -8)
bill(806, 756, 185, 30)
bill(660, 806, 175, -22)
for cx, cy, cr in ((905, 872, 34), (962, 884, 28), (858, 890, 26), (1006, 862, 24), (930, 842, 22)):
    coin(cx, cy, cr)
# money bag
bag = Image.new("RGBA", (190, 210), (0, 0, 0, 0))
bd = ImageDraw.Draw(bag)
bd.polygon([(95, 26), (66, 74), (124, 74)], fill=(150, 116, 60, 255))
bd.ellipse([18, 62, 172, 204], fill=(178, 138, 74, 255), outline=(120, 90, 40, 255), width=4)
bd.rectangle([64, 58, 126, 76], fill=(120, 90, 40, 255))
fbag = ImageFont.truetype(FONT, 74)
bd.text((95, 138), "$", font=fbag, anchor="mm", fill=(255, 244, 200, 255))
img.paste(bag, (1064, 690), bag)
d = ImageDraw.Draw(img, "RGBA")
# sparkles around the ghost
for sx, sy, sr in ((716, 268, 16), (1218, 330, 13), (1196, 640, 11), (690, 470, 10)):
    d.polygon([(sx, sy - sr), (sx + sr * 0.28, sy - sr * 0.28), (sx + sr, sy), (sx + sr * 0.28, sy + sr * 0.28),
               (sx, sy + sr), (sx - sr * 0.28, sy + sr * 0.28), (sx - sr, sy), (sx - sr * 0.28, sy - sr * 0.28)],
              fill=(255, 240, 150, 255))

# ---------- meme captions ----------
def caption(lines, y_top, base_size):
    yy = y_top
    for text, size in lines:
        f = ImageFont.truetype(FONT, size)
        while d.textlength(text, font=f) > W - 70 and size > 30:
            size -= 4
            f = ImageFont.truetype(FONT, size)
        d.text((W / 2, yy), text, font=f, anchor="ma", fill=(255, 255, 255, 255),
               stroke_width=max(4, size // 11), stroke_fill=(0, 0, 0, 255))
        yy += int(size * 1.18)
    return yy

caption([("STILL WAITING FOR GTA 6…", 96)], 26, 96)
caption([("MY AI AGENT ALREADY GOT PAID", 84), ("ON make.fun", 118)], 1012, 118)

img.save("meme.png")
print("saved meme.png", img.size)
