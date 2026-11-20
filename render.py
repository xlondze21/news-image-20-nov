#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news infographic as entry.png.

Everything is drawn with Pillow: no network access, no clock, no random
numbers. The same input always produces the same PNG bytes, so the
entrypoint can run the generator twice and get an identical file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "entry.png")

PAPER = (248, 244, 236)
INK = (22, 25, 32)
MUTED = (56, 66, 82)
NAVY = (30, 45, 80)
NAVY_DEEP = (20, 32, 60)
SCARLET = (198, 60, 45)
SCARLET_DARK = (152, 42, 32)
GOLD = (186, 124, 32)
GRAY = (108, 115, 130)
RULE = (216, 207, 190)
CARD = (255, 255, 255)
SKY = (150, 199, 253)
LEAF = (34, 139, 92)
UP = (24, 165, 75)
DOWN = (248, 113, 113)


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


def bold(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return load_font("DejaVuSans.ttf", size)


def measure(draw, text, font):
    return draw.textlength(text, font=font)


def split_lines(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if measure(draw, trial, font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw, x, y, text, font, width, color, spacing=None, limit=None):
    lines = split_lines(draw, text, font, width)
    if limit is not None:
        lines = lines[:limit]
    step = spacing if spacing is not None else int(font.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += step
    return y


def spaced_text(draw, x, y, text, font, color, gap=3):
    """Draw text with extra space between characters; returns end x."""
    cursor = x
    for char in text:
        draw.text((cursor, y), char, font=font, fill=color)
        cursor += measure(draw, char, font) + gap
    return cursor


def five_point_star(draw, cx, cy, radius, color):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.45
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=color)


# ------------------------------------------------------------------ icons
def draw_scales(draw, x, y, w, h):
    """Scales of justice on a deep-navy panel (the ICJ hero art)."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_DEEP)
    # faint columns behind the scales
    for col_x in (x + 14, x + w - 26):
        draw.rectangle([col_x, y + 18, col_x + 12, y + h - 18],
                       fill=(42, 60, 100))
    cx = x + w // 2
    top = y + 16
    base_y = y + h - 22
    # post, beam and base
    draw.line([cx, top + 6, cx, base_y], fill=GOLD, width=5)
    draw.line([cx - 34, top + 10, cx + 34, top + 10], fill=GOLD, width=5)
    draw.line([cx - 26, base_y, cx + 26, base_y], fill=GOLD, width=5)
    five_point_star(draw, cx, top, 7, GOLD)
    # chains and pans
    for side in (-1, 1):
        px = cx + side * 34
        draw.line([px, top + 10, px - 12, top + 44], fill=GOLD, width=2)
        draw.line([px, top + 10, px + 12, top + 44], fill=GOLD, width=2)
        draw.arc([px - 16, top + 38, px + 16, top + 66], 0, 180, fill=GOLD,
                 width=4)
        draw.line([px - 16, top + 52, px + 16, top + 52], fill=GOLD, width=4)
    # small gavel bar at the bottom
    draw.rectangle([cx - 18, base_y + 8, cx + 18, base_y + 13], fill=GOLD)


def draw_skyline(draw, x, y, size):
    """Three flagpoles over a dusk skyline (the Shenzhen summit)."""
    draw.rectangle([x, y, x + size, y + size], fill=(13, 148, 136))
    draw.ellipse([x + size - 36, y + 12, x + size - 14, y + 34],
                 fill=(253, 224, 71))
    bottom = y + size - 14
    for bx, bw, bh in ((10, 18, 30), (32, 14, 46), (50, 18, 26), (72, 14, 38)):
        draw.rectangle([x + bx, bottom - bh, x + bx + bw, bottom], fill=CARD)
    draw.line([x + 10, bottom, x + size - 10, bottom], fill=CARD, width=3)
    # three small flags on poles above the roofs
    for fx, flag in ((x + 20, SCARLET), (x + 48, GOLD), (x + 76, (37, 99, 235))):
        draw.line([fx, y + 8, fx, y + 26], fill=CARD, width=2)
        draw.polygon([(fx, y + 8), (fx + 12, y + 12), (fx, y + 16)], fill=flag)


def draw_chart(draw, x, y, size):
    """Rising market line with bars (the Anthropic debut)."""
    draw.rectangle([x, y, x + size, y + size], fill=(254, 243, 199))
    # bars
    base = y + size - 16
    for i, bh in enumerate((18, 26, 22, 34, 30, 44)):
        bx = x + 10 + i * 14
        draw.rectangle([bx, base - bh, bx + 9, base], fill=(253, 196, 64))
    # rising line with an arrowhead
    pts = [(x + 8, y + size - 34), (x + 26, y + size - 46), (x + 44, y + 38),
           (x + 62, y + 44), (x + 80, y + 22)]
    draw.line(pts, fill=UP, width=5, joint="curve")
    hx, hy = pts[-1]
    draw.polygon([(hx, hy - 8), (hx + 10, hy + 2), (hx - 2, hy + 8)], fill=UP)


def draw_dome(draw, x, y, size):
    """A capitol dome (the Senate war-powers vote)."""
    draw.rectangle([x, y, x + size, y + size], fill=(219, 234, 254))
    cx = x + size // 2
    # dome
    draw.pieslice([cx - 30, y + 12, cx + 30, y + 62], 180, 360,
                  fill=(37, 99, 235))
    draw.rectangle([cx - 2, y + 4, cx + 2, y + 14], fill=(37, 99, 235))
    # drum and columns
    draw.rectangle([cx - 30, y + 58, cx + 30, y + 66], fill=(37, 99, 235))
    for i in range(5):
        col_x = x + 14 + i * 14
        draw.rectangle([col_x, y + 66, col_x + 6, y + size - 20],
                       fill=(37, 99, 235))
    draw.rectangle([x + 10, y + size - 20, x + size - 10, y + size - 14],
                   fill=(37, 99, 235))


def draw_drone(draw, x, y, size):
    """A quadcopter drone (the UK drone package for Ukraine)."""
    draw.rectangle([x, y, x + size, y + size], fill=(51, 65, 85))
    cx, cy = x + size // 2, y + size // 2
    # arms and rotors
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        ax, ay = cx + sx * 26, cy + sy * 22
        draw.line([cx, cy, ax, ay], fill=(203, 213, 225), width=3)
        draw.ellipse([ax - 11, ay - 4, ax + 11, ay + 4], fill=(148, 163, 184))
    # body
    draw.ellipse([cx - 14, cy - 10, cx + 14, cy + 10], fill=(226, 232, 240))
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=SCARLET)


def draw_leaf(draw, x, y, size):
    """A leaf on green (the COP31 climate strip)."""
    draw.rectangle([x, y, x + size, y + size], fill=LEAF)
    cx, cy = x + size // 2, y + size // 2
    draw.ellipse([cx - 20, cy - 26, cx + 20, cy + 26], fill=(134, 239, 172))
    draw.line([cx - 16, cy + 22, cx + 16, cy - 22], fill=LEAF, width=3)
    draw.line([cx, cy, cx + 14, cy - 6], fill=LEAF, width=2)
    draw.line([cx, cy + 6, cx - 12, cy + 2], fill=LEAF, width=2)


# ------------------------------------------------------------------ page
def build(target=None):
    target = target or TARGET
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, CANVAS_W, 112], fill=NAVY)
    d.rectangle([0, 112, CANVAS_W, 116], fill=GOLD)
    spaced_text(d, 36, 18, "THE WORLD IN ONE DAY", bold(20), GOLD, gap=4)
    d.text((36, 44), "FRIDAY, 20 NOVEMBER 2026", font=bold(50), fill=CARD)

    # ---- hero: the ICJ genocide verdict
    hero_y = 132
    d.text((36, hero_y), "TOP STORY  —  THE HAGUE", font=bold(20), fill=SCARLET)
    cursor = hero_y + 30
    cursor = paragraph(d, 36, cursor, "World Court: Myanmar guilty of genocide",
                       bold(46), 600, INK, spacing=52, limit=2)
    cursor += 8
    paragraph(d, 36, cursor,
              "The ICJ ruled 9–6 that Myanmar committed genocide in the "
              "2017 Rakhine crackdown — the first time the court has held "
              "a state responsible. Myanmar has two years to pay restitution.",
              regular(21), 600, MUTED, spacing=27, limit=4)
    draw_scales(d, 668, 132, 320, 236)
    d.line([36, 392, CANVAS_W - 36, 392], fill=RULE, width=2)

    # ---- four-card grid
    d.text((36, 408), "ALSO TODAY", font=bold(20), fill=NAVY)
    cards = [
        (draw_skyline, "ASIA", "Trump, Xi, Putin issue peace declaration",
         "After their first three-way summit in Shenzhen, the three "
         "leaders issue a joint declaration on the APEC sidelines."),
        (draw_chart, "TECH", "Anthropic debuts on Nasdaq, up 17%",
         "The first frontier AI lab to go public (ticker ANT) closes 17% "
         "above its $83 IPO price after a record $81.3B raise."),
        (draw_dome, "MIDDLE EAST", "Senate rejects Iran war-powers vote",
         "The Senate votes 51–48 against curbing the war as its cost tops "
         "$48B; Iran widens Gulf attacks."),
        (draw_drone, "EUROPE", "UK pledges 1,000+ drones for Ukraine",
         "A £260m package as Russia hits Kyiv bridges, damaging the "
         "Austrian and Dutch embassies."),
    ]
    gx, gy = 36, 440
    cw, ch, gap = 468, 196, 16
    for i, (art, kicker, head, body) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=RULE, width=2)
        art(d, x + 14, yy + 14, 92)
        tx = x + 120
        d.text((tx, yy + 14), kicker, font=bold(16), fill=SCARLET)
        after_head = paragraph(d, tx, yy + 36, head, bold(24), cw - 134, INK,
                               spacing=28, limit=2)
        paragraph(d, tx, after_head + 4, body, regular(16), cw - 134, MUTED,
                  spacing=20, limit=3)

    # ---- climate strip
    strip_y = gy + 2 * ch + gap + 14
    d.rectangle([36, strip_y, CANVAS_W - 36, strip_y + 60], fill=CARD,
                outline=RULE, width=2)
    draw_leaf(d, 48, strip_y + 6, 48)
    d.text((112, strip_y + 6), "CLIMATE", font=bold(16), fill=SCARLET)
    d.text((112, strip_y + 26), "Fossil fuels cut from COP31 draft deal",
           font=bold(22), fill=INK)

    # ---- markets ticker card (US closes of 19 Nov, labelled as such)
    tick_y = strip_y + 60 + 8
    d.rectangle([36, tick_y, CANVAS_W - 36, tick_y + 64], fill=CARD,
                outline=RULE, width=2)
    d.text((54, tick_y + 8), "US MARKETS — CLOSES 19 NOV", font=bold(17),
           fill=NAVY)
    note = "FINAL CLOSES, THU 19 NOV"
    d.text((CANVAS_W - 54 - measure(d, note, regular(13)), tick_y + 10),
           note, font=regular(13), fill=GRAY)
    marks = [("DOW", "49,097.06", "-2.19%"),
             ("S&P 500", "7,175.83", "-2.02%"),
             ("NASDAQ", "23,879.20", "-2.25%"),
             ("GOLD · DEC", "$3,685.50", "-1.51%"),
             ("BRENT · JAN", "$91.98", "+0.03%")]
    col_w = (CANVAS_W - 72 - 36) // 5
    for i, (name, val, chg) in enumerate(marks):
        cx = 54 + i * col_w
        d.text((cx, tick_y + 30), name, font=bold(13), fill=GRAY)
        d.text((cx, tick_y + 46), val, font=bold(17), fill=INK)
        vx = cx + measure(d, val, bold(17)) + 6
        d.text((vx, tick_y + 46), chg, font=bold(15),
               fill=UP if chg.startswith("+") else DOWN)

    # ---- footer
    d.text((36, CANVAS_H - 24),
           "Compiled from wire reports  ·  20 November 2026  ·  Drawn by program, no photos",
           font=regular(15), fill=GRAY)

    img.save(target, format="PNG", optimize=True)
    print("wrote", target, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    build()
