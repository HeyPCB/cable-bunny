"""Writes boards/merch_cable_bunny/board.json: the USB-C cable tester bunny (heypcb.ai merch 04).

    "$KICAD_PYTHON" boards/merch_cable_bunny/make_brief.py

Plug both ends of a USB-C cable into the bunny's feet and boop its nose: its ears light one LED per
line the cable actually carries (VBUS, GND, CC on the left; D+, D-, SBU on the right) and a heart says
the coin cell is good. No MCU: a button, a Schottky, resistors and LEDs. Edit this file, not
board.json. Frame 60 x 98 mm, origin top-left, y down.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import merch_kit as K  # noqa: E402

SLUG = "cable-bunny"
W, H = 60.0, 98.0
CX = 30.0
EAR_TILT = 7.0

BLOCKS = [
    {"block": "merch_cr2032", "as": "bat", "title": "CR2032 in the belly"},
    {"block": "merch_press_power", "as": "nose", "title": "Boop the nose: power while pressed, B5819W blocks back-feed",
     "nets": {"VSW": "VSW", "VTEST": "VTEST"}},
    {"block": "merch_usbc_test_source", "as": "src", "title": "Left foot: drives every line (150 ohm each)",
     "nets": {"VTEST": "VTEST"}},
    {"block": "merch_usbc_test_sink", "as": "snk", "title": "Right foot: one LED per line that arrives",
     "nets": {"VTEST": "VTEST", "CABLE_GND": "CABLE_GND"}},
    {"block": "gpio_led", "as": "heart", "title": "Heart: the cell is good", "nets": {"SIG": "VTEST"},
     "values": {"D?": "Red", "R?": "330"}},
]

# LED order along each ear, top to bottom: (sink LED token, label)
LEFT_EAR = [("D1?", "VBUS"), ("D6?", "GND"), ("D2?", "CC")]
RIGHT_EAR = [("D3?", "D+"), ("D4?", "D-"), ("D5?", "SBU")]
EAR_ROWS = [10.0, 16.0, 22.0]

# ---------------------------------------------------------------------------------------- outline
ear_l = K.Shape.ellipse(18.0, 19.0, 7.4, 18.2, -EAR_TILT)
ear_r = K.Shape.ellipse(W - 18.0, 19.0, 7.4, 18.2, EAR_TILT)
head = K.Shape.ellipse(CX, 42.0, 20.0, 15.0)
body = K.Shape.rect(10.0, 52.0, 50.0, 97.0, r=9.0)
outline = (ear_l | ear_r | head | body).rounded(1.5)


def ear_axis_x(side, y):
    """The ear's centre line at height y (the ears lean out by EAR_TILT degrees)."""
    t = math.tan(math.radians(EAR_TILT)) * (y - 19.0)
    return (18.0 + t) if side < 0 else (W - 18.0 - t)


# ---------------------------------------------------------------------------------------- parts
parts = K.design_footprints(BLOCKS, os.path.join(os.path.dirname(HERE), "..", "blocks"))
L = K.Layout(parts)
labels = []
for side, ear in ((-1, LEFT_EAR), (1, RIGHT_EAR)):
    for (tok, name), y in zip(ear, EAR_ROWS):
        ax = ear_axis_x(side, y)
        L.lock("snk:%s" % tok, ax - 2.4, y, 0, "%s LED in the %s ear" % (name, "left" if side < 0 else "right"))
        labels.append((name, ax + 1.0, y))
L.lock("nose:SW?", CX, 46.4, 0, "the nose: boop to test")
L.lock("heart:D?", CX, 55.2, 0, "the heart: the cell is good")
L.lock("heart:R?", CX + 4.6, 55.2, 0, "")
L.lock("bat:BT?", CX, 70.0, 0, "the cell in the belly")
L.lock("bat:C?", CX, 84.4, 0, "reservoir")
L.lock("nose:D?", CX, 91.0, 90, "back-feed Schottky between the feet")
L.lock("src:J?", 20.0, 97.0 + 0.6 - 4.2, 0, "left foot: the source end", overhang=True)
L.lock("snk:J?", 40.0, 97.0 + 0.6 - 4.2, 0, "right foot: the far end", overhang=True)
for i in range(5):
    L.lock("src:R%d?" % (i + 1), 15.0 + 1.9 * i, 84.6, 90, "150 ohm line driver")
for i in range(6):
    L.lock("snk:R%d?" % (i + 1), 35.6 + 1.9 * i, 84.6, 90, "LED resistor")

# ---------------------------------------------------------------------------------------- art
art = []
for name, x, y in labels:
    art += K.text(name, x, y, size=0.9, justify="left", name="label_" + name)
art += K.text("power", ear_axis_x(-1, 28.5), 28.0, size=0.9, name="ear_l_title")
art += K.text("data", ear_axis_x(1, 28.5), 28.0, size=0.9, name="ear_r_title")
# face: eyes, gold cheeks, a mouth under the nose button, whiskers
for sx in (-1, 1):
    art += K.silk_fill(K.Shape.ellipse(CX + sx * 7.5, 39.5, 1.5, 2.1), "eye")
    art += K.gold(K.Shape.ellipse(CX + sx * 11.6, 46.0, 2.6, 1.6), "cheek")
    for dy in (-0.9, 0.9):
        art += K.silk_line([(CX + sx * 5.2, 49.6 + dy), (CX + sx * 9.6, 49.6 + dy * 2.2)], "whisker", 0.2)
art += K.silk_line(K.arc_points(CX - 1.1, 50.3, 1.1, 0, 180, 10) + K.arc_points(CX + 1.1, 50.3, 1.1, 0, 180, 10)[1:],
                   "mouth", 0.22)
heart = K.heart(CX, 55.4, 6.4)
art += K.silk_ring(heart, "heart", 0.2)
art += K.text("heypcb.ai", CX, 82.2, size=0.8, name="brand_front")
# back: QR, the legend, the brand
art += K.qr(K.world_url(SLUG), CX, 68.0, size=12.0, side="B")
legend = ["plug both ends of a USB-C", "cable into my feet, boop my nose",
          "heart: my battery is good",
          "VBUS + GND + CC: it charges",
          "+ D+ and D-: it carries USB data",
          "+ SBU: full-featured (USB3, TB, DP)"]
for i, line in enumerate(legend):
    art += K.text(line, CX, 33.0 + 2.0 * i, size=1.0, side="B", name="legend%d" % i)
art += K.text("heypcb.ai", CX, 80.4, size=1.3, side="B", bold=True, name="brand_back")

keep = {}
for i, it in enumerate(a for a in art if "F.Cu" in a.get("layers", [])):
    keep["gold%d" % i] = K.Shape.poly(it["points"]).offset(0.3)
L.check(outline, edge=0.5, keep=keep)

brief = {
    "name": "cable_bunny",
    "title": "Cable Bunny - USB-C cable tester: VBUS, GND, CC, D+, D-, SBU, CR2032",
    "revision": "A",
    "brief": "A bunny-shaped USB-C cable tester with no MCU. Both ends of a cable plug into the two USB-C "
             "receptacles that are its feet; pressing its nose connects a CR2032 through a B5819W to every "
             "line of the first receptacle through 150 ohm, and every line that reaches the second receptacle "
             "lights its own LED through 220 ohm in the bunny's ears (VBUS, GND, CC; D+, D-, SBU). A heart LED "
             "shows the cell is good. 2 layers, single-sided SMT, white mask, black silk, ENIG.",
    "blocks": BLOCKS,
    "pwrFlags": ["GND", "VBAT"],
    "netClasses": [],
    "board": {
        "width": W, "height": H, "corner_radius": 0.0, "layers": 2, "origin": [100.0, 100.0],
        "shape": {"type": "polygon", "points": K.outline_points(outline), "fillet": 0},
        "rules": {"clearance": 0.2, "track": 0.2, "via": [0.6, 0.3], "edge_clearance": 0.5,
                  "hole_to_hole": 0.5, "min_through_hole": 0.3, "min_track": 0.15},
        "finish": {"mask": "White", "silk": "Black", "copper": "ENIG",
                   "why": "a white bunny drawn in black; gold cheeks"},
        "unpoured": ["F.Cu"],
        "notes": "2 layers; the face is unpoured, GND (the cell's negative) poured on the back.",
    },
    "placement": L.locks,
    "route": {"passes": 30, "fanout": True, "solve_s": 240},
    "stitch_pitch": 6.0,
    "silk": {"designators": "hide",
             "title": [{"text": "Cable Bunny", "y": 47.0, "size": 1.8, "bold": True},
                       {"text": "USB-C cable tester  rev {revision}", "y": 49.8, "size": 0.9}]},
    "art": art,
    "captions": {"done_3d": "Cable Bunny: plug a cable into its feet, boop its nose, read its ears."},
}
K.write_brief(os.path.join(HERE, "board.json"), brief)
print("wrote board.json: %d outline points, %d art items, %d locks, QR -> %s"
      % (len(brief["board"]["shape"]["points"]), len(art), len(L.locks), K.world_url(SLUG)))
