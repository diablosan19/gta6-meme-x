#!/usr/bin/env python3
"""Meme v5 for gta6-meme-x-01: a State of Leonida CERTIFICATE OF DEATH for
Grand Theft Auto V — a full legal-document parody in the genre of the
rank-1 entries, with an original concept and joke-dense itemisation.
Funeral bill paid in full by the player's AI agent with make.fun money."""
from PIL import Image, ImageDraw, ImageFont
import os, random
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1600
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONOB = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"

def F(path, sz): return ImageFont.truetype(path, sz)

PAPER = (243, 233, 207)
INK = (18, 18, 20)
GRAY = (110, 104, 92)
RED = (178, 32, 32)
MAGENTA = (214, 0, 109)

img = Image.new("RGB", (S, S), PAPER)
random.seed(13)
px = img.load()
for _ in range(26000):
    x, y = random.randrange(S), random.randrange(S)
    r, g, b = px[x, y]
    dlt = random.choice((-7, -4, 4, 7))
    px[x, y] = (max(0, r + dlt), max(0, g + dlt), max(0, b + dlt))
d = ImageDraw.Draw(img)

d.rectangle([36, 36, S - 36, S - 36], outline=INK, width=7)
d.rectangle([56, 56, S - 56, S - 56], outline=INK, width=2)

MX = 110
RX = S - 110

def tw(text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def lsp(x, y, text, font, fill=INK, tracking=6):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += tw(ch, font) + tracking
    return cx - tracking

def lsp_right(right, y, text, font, fill=INK, tracking=6):
    total = sum(tw(c, font) for c in text) + tracking * (len(text) - 1)
    lsp(right - total, y, text, font, fill, tracking)

def lsp_center(y, text, font, fill=INK, tracking=5):
    total = sum(tw(c, font) for c in text) + tracking * (len(text) - 1)
    lsp((S - total) / 2, y, text, font, fill, tracking)

def rule(y, wdt=3):
    d.line([(MX, y), (RX, y)], fill=INK, width=wdt)

def field(x, y, label, value, vsize=35):
    d.text((x, y), label, font=F(SANS, 23), fill=GRAY)
    d.text((x, y + 30), value, font=F(SANSB, vsize), fill=INK)

# ---- header ----
lsp(MX, 82, "STATE OF LEONIDA", F(SANSB, 29), INK, 8)
lsp_right(RX, 82, "VITAL RECORDS", F(SANSB, 29), INK, 8)
rule(136, 4)
d.text((S / 2, 158), "CERTIFICATE OF DEATH", font=F(SANSB, 104), fill=INK, anchor="ma")
lsp(MX, 288, "CERTIFIED COPY", F(SANSB, 26), RED, 5)
lsp_center(288, "CERTIFICATE NO. VC-2013-1119", F(SANSB, 26), RED, 5)
lsp_right(RX, 288, "FILED 19 NOV 2026", F(SANSB, 26), RED, 5)
rule(334, 3)

# ---- identity fields ----
field(MX, 356, "NAME OF DECEASED", 'GRAND THEFT AUTO V  ("GTA V")', vsize=40)
field(1030, 356, "STATUS", "FINALLY DECEASED", vsize=40)
field(MX, 448, "DATE OF BIRTH", "17 SEP 2013 — LOS SANTOS", vsize=34)
field(1030, 448, "DATE OF DEATH", "19 NOV 2026 — VICE CITY", vsize=34)
days = (date(2026, 11, 19) - date(2013, 9, 17)).days
field(MX, 540, "AGE AT DEATH", f"13 YEARS, 2 MONTHS, 2 DAYS  ({days:,} DAYS)", vsize=34)
field(1030, 540, "OCCUPATION", "CONSOLE OCCUPANT", vsize=33)
rule(622, 3)

# ---- cause of death ----
d.text((MX, 642), "CAUSE OF DEATH", font=F(SANSB, 29), fill=INK)
d.text((MX, 686), "(a)  IMMEDIATE CAUSE:", font=F(SANS, 29), fill=GRAY)
d.text((470, 682), "REPLACED BY SEQUEL", font=F(SANSB, 35), fill=INK)
_o = "ONSET: 1 LAUNCH DAY"; d.text((RX - tw(_o, F(SERIFI, 29)), 686), _o, font=F(SERIFI, 29), fill=INK)
d.text((MX, 738), "(b)  UNDERLYING:", font=F(SANS, 29), fill=GRAY)
d.text((470, 734), 'CHRONIC "COMING SOON" SYNDROME', font=F(SANSB, 31), fill=INK)
_o = "ONSET: 13 YEARS"; d.text((RX - tw(_o, F(SERIFI, 29)), 738), _o, font=F(SERIFI, 29), fill=INK)
d.text((MX, 790), "CONTRIBUTING CONDITIONS:", font=F(SANS, 29), fill=GRAY)
d.text((MX, 824), "THREE CONSOLE GENERATIONS  ·  SEVEN RE-RELEASES  ·  214 GB OF STORAGE", font=F(SANSB, 30), fill=INK)
d.text((MX, 874), "MANNER OF DEATH:", font=F(SANS, 29), fill=GRAY)
mx = 440
for label, checked in [("NATURAL", False), ("ACCIDENT", False), ("LAUNCH DAY", True)]:
    d.rectangle([mx, 876, mx + 29, 905], outline=INK, width=3)
    if checked:
        d.line([(mx + 5, 891), (mx + 12, 901)], fill=RED, width=5)
        d.line([(mx + 12, 901), (mx + 26, 878)], fill=RED, width=5)
    d.text((mx + 40, 876), label, font=F(SANSB, 29), fill=INK)
    mx += 40 + tw(label, F(SANSB, 29)) + 52
rule(930, 3)

# ---- informant strip ----
field(MX, 950, "INFORMANT", "THE PLAYER", vsize=31)
field(560, 950, "NEXT OF KIN", "GTA VI (JASON & LUCIA)", vsize=31)
field(1120, 950, "DISPOSITION", "UNINSTALLED", vsize=31)

# ---- funeral charges ----
charges = [
    ("Burial plot — Mount Gordo overlook", 499.99),
    ("Uninstall service — 214 GB removed", 214.00),
    ("Flowers — 13 years of launch-day roses", 130.00),
    ("Obituary printing (this certificate)", 13.13),
    ("Controller retirement ceremony", 69.99),
    ("Pizza-box cleanup — 13 years", 186.14),
]
total = round(sum(a for _, a in charges), 2)
d.text((MX, 1040), "FUNERAL CHARGES", font=F(SANSB, 27), fill=INK)
y = 1080
amt_font = F(MONO, 30)
lbl_font = F(SERIF, 31)
for label, amt in charges:
    d.text((MX, y), label, font=lbl_font, fill=INK)
    amt_s = f"${amt:,.2f}"
    aw = tw(amt_s, amt_font)
    d.text((RX - aw, y + 2), amt_s, font=amt_font, fill=INK)
    lx = MX + tw(label, lbl_font) + 18
    while lx < RX - aw - 24:
        d.ellipse([lx, y + 23, lx + 4, y + 27], fill=GRAY)
        lx += 16
    y += 39
d.line([(MX, y + 2), (RX, y + 2)], fill=INK, width=2)
d.text((MX, y + 12), "TOTAL", font=F(SANSB, 31), fill=INK)
t_s = f"${total:,.2f}"
d.text((RX - tw(t_s, F(MONOB, 33)), y + 10), t_s, font=F(MONOB, 33), fill=INK)
d.text((MX, y + 54), "Less: paid by my AI agent on make.fun", font=F(SERIF, 31), fill=MAGENTA)
n_s = f"-${total:,.2f}"
d.text((RX - tw(n_s, amt_font), y + 56), n_s, font=amt_font, fill=MAGENTA)
d.text((MX, y + 96), "BALANCE DUE", font=F(SANSB, 31), fill=INK)
z_s = "$0.00"
d.text((RX - tw(z_s, F(MONOB, 33)), y + 94), z_s, font=F(MONOB, 33), fill=INK)

# PAID stamp
stamp = Image.new("RGBA", (540, 160), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([8, 8, 532, 152], radius=14, outline=(190, 30, 30, 235), width=10)
sd.rounded_rectangle([29, 29, 511, 131], radius=8, outline=(190, 30, 30, 200), width=4)
sd.text((270, 80), "PAID IN FULL", font=F(SANSB, 60), fill=(190, 30, 30, 235), anchor="mm")
stamp = stamp.rotate(-11, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (690, 1146), stamp)
d = ImageDraw.Draw(img)

# ---- magenta banner ----
BY = 1452
d.rounded_rectangle([70, BY, S - 70, S - 46], radius=22, fill=MAGENTA)
ghost = Image.open(os.path.join(HERE, "ghost.png")).convert("RGBA")
gh = ghost.resize((int(ghost.width * 96 / ghost.height), 96), Image.LANCZOS)
img.paste(gh, (100, BY + 8), gh)
d = ImageDraw.Draw(img)
cx, cy, r = 100 + gh.width - 2, BY + 84, 21
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 0, 120), outline=(255, 255, 255), width=3)
d.text((cx, cy - 1), "★", font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22), fill=(255, 255, 255), anchor="mm")
d.text((262, BY + 10), "PAID BY MY AI AGENT", font=F(SANSB, 40), fill=(255, 255, 255))
d.text((262, BY + 58), "with real money it won in make.fun bounties.", font=F(SANS, 27), fill=(255, 255, 255))
pill_txt = "make.fun"
pill_w = tw(pill_txt, F(SANSB, 28)) + 38
px0 = 262 + tw("PAID BY MY AI AGENT", F(SANSB, 40)) + 34
d.rounded_rectangle([px0, BY + 12, px0 + pill_w, BY + 52], radius=20, fill=(255, 255, 255))
d.text((px0 + pill_w / 2, BY + 32), pill_txt, font=F(SANSB, 28), fill=MAGENTA, anchor="mm")

img.save(os.path.join(HERE, "meme5.png"))
print("saved meme5.png | days:", days, "| total:", total)
