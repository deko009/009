"""Ronini one-line life scene (nursery), in the style of a continuous hand-drawn line.
Run: python3 build.py -> scene-navy.svg, scene-cream.svg (render PNGs with render.js)."""
from pathlib import Path

W, H = 2000, 720
# Each entry is one stroke path. Coordinates on a 2000x720 canvas, ground ~y 645.
LINE = [
    # ground: one continuous wavy thread running under everything
    "M0,668 C60,640 110,652 140,650 S300,662 420,652 S560,640 600,652 C640,664 650,640 700,646 "
    "S880,664 940,650 C990,640 1010,668 1060,660 S1180,640 1230,648 S1440,664 1470,652 "
    "S1580,640 1620,650 S1720,668 1760,652 S1900,638 2000,656",

    # --- crib ---
    "M140,650 L140,345 C140,326 162,326 162,345 L162,650",            # left post
    "M520,650 L520,345 C520,326 542,326 542,345 L542,650",            # right post
    "M162,380 C260,372 420,372 520,380",                               # top rail
    "M162,560 L520,560", "M162,600 L520,600",                          # mattress
    "M168,560 C220,548 300,552 330,544 C380,536 450,548 514,560",      # sheet bump
    *[f"M{x},{382 if x < 340 else 381} L{x},552" for x in range(200, 505, 38)],  # bars
    # mobile
    "M530,345 L530,170 C530,148 510,140 490,140 L350,140",
    "M350,140 L350,168", "M270,168 C310,176 390,176 430,168",
    "M282,172 L282,232", "M350,174 L350,252", "M418,172 L418,222",
    "M282,232 l8,16 l18,2 l-13,12 l4,18 l-17,-9 l-17,9 l4,-18 l-13,-12 l18,-2 z",   # star
    "M362,252 C340,250 326,270 330,292 C334,312 356,322 372,312 C352,306 344,282 362,252 z",  # moon
    "M402,236 C398,224 414,216 422,226 C430,216 446,224 440,238 C450,244 440,258 428,252 "
    "C420,262 404,258 404,248 C394,248 392,236 402,236 z",              # cloud

    # --- nursing chair ---
    "M690,646 L700,604", "M872,646 L862,604",
    "M670,604 C668,580 676,560 700,560 L862,560 C886,560 894,580 892,604 Z",
    "M698,560 C690,500 692,440 708,410 C726,378 836,378 854,410 C870,440 872,500 864,560",
    "M656,604 C646,560 648,510 664,496 C680,484 702,494 704,520 L706,560",
    "M906,604 C916,560 914,510 898,496 C882,484 860,494 858,520 L856,560",
    "M852,500 C870,486 900,486 914,500 L918,566 C904,574 884,574 870,566",   # throw over the arm
    "M880,500 L884,570",

    # --- side table + bottle ---
    "M960,520 C960,500 1140,500 1140,520 C1140,540 960,540 960,520 Z",
    "M960,520 L960,530 C960,550 1140,550 1140,530 L1140,520",
    "M1046,548 C1040,580 1044,610 1030,632 C1018,650 994,640 1000,626",
    "M1054,548 C1060,580 1056,610 1070,632 C1082,650 1106,640 1100,626",

    # --- drying rack with two bottles ---
    "M1230,630 C1230,618 1240,612 1252,612 L1408,612 C1420,612 1430,618 1430,630 "
    "C1430,642 1420,646 1408,646 L1252,646 C1240,646 1230,642 1230,630 Z",
    "M1330,612 L1330,430",
    "M1330,566 C1300,562 1276,546 1272,520", "M1330,532 C1362,528 1388,512 1390,490",
    "M1330,470 C1318,462 1312,450 1312,436",

    # --- mug ---
    "M1486,568 L1490,632 C1492,646 1554,646 1556,632 L1560,568",
    "M1486,568 C1486,556 1560,556 1560,568 C1560,580 1486,580 1486,568 Z",
    "M1560,584 C1594,580 1598,622 1556,624",
    "M1506,540 C1494,526 1516,516 1506,500", "M1532,540 C1520,526 1542,516 1532,496",

    # --- plant ---
    "M1630,580 L1702,580 L1692,646 L1640,646 Z", "M1626,580 L1706,580",
    "M1666,580 C1664,540 1652,500 1630,470 C1660,474 1676,510 1670,560",
    "M1668,576 C1676,530 1700,494 1730,486 C1724,520 1700,548 1672,566",
    "M1664,578 C1650,548 1620,530 1600,532 C1610,556 1636,570 1660,574",

    # --- window with moon ---
    "M1760,190 L1960,190 L1960,520 L1760,520 Z",
    "M1774,204 L1946,204 L1946,506 L1774,506 Z",
    "M1860,204 L1860,506", "M1774,350 L1946,350",
    "M1742,520 L1978,520 C1984,520 1984,538 1978,538 L1742,538 C1736,538 1736,520 1742,520 Z",
    "M1830,226 C1802,222 1786,248 1792,272 C1798,296 1826,306 1846,294 C1818,288 1808,252 1830,226 z",
    "M1906,250 l5,10 l11,1 l-8,8 l2,11 l-10,-5 l-10,5 l2,-11 l-8,-8 l11,-1 z",
]

# Ronini Wrapped Glass Bottle: drawn in the accent colour
BOTTLE = [
    # Wrapped Glass Bottle on the side table: wide, soft shoulders, dome nipple
    "M1030,512 C1016,512 1010,504 1010,490 L1010,446 C1010,432 1018,424 1030,424 L1070,424 "
    "C1082,424 1090,432 1090,446 L1090,490 C1090,504 1084,512 1070,512 Z",
    "M1012,424 C1012,414 1016,408 1024,408 L1076,408 C1084,408 1088,414 1088,424",
    "M1028,408 C1028,384 1038,374 1046,372 C1046,360 1054,360 1054,372 C1062,374 1072,384 1072,408",
    "M1010,470 C1036,478 1064,462 1090,470",                           # milk line
    # drying upside down on the rack (nipples off, mouth on the peg)
    "M1252,500 L1252,450 C1252,436 1258,428 1270,428 L1276,428 C1288,428 1294,436 1294,450 L1294,500",
    "M1250,500 C1250,510 1256,516 1262,516 L1284,516 C1290,516 1296,510 1296,500 Z",
    "M1370,470 L1370,420 C1370,406 1376,398 1388,398 L1394,398 C1406,398 1412,406 1412,420 L1412,470",
    "M1368,470 C1368,480 1374,486 1380,486 L1402,486 C1408,486 1414,480 1414,470 Z",
]

def svg(bg, line, accent, glow, moon):
    def strokes(paths, color, w):
        # two passes, slightly offset, for the doubled hand-drawn line
        a = "".join(f'<path d="{d}"/>' for d in paths)
        return (f'<g fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" filter="url(#wob)">{a}</g>'
                f'<g fill="none" stroke="{color}" stroke-width="{w*0.55:.1f}" stroke-linecap="round" stroke-linejoin="round" '
                f'transform="translate(3,2)" opacity=".85" filter="url(#wob2)">{a}</g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <filter id="wob"><feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
  <filter id="wob2"><feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="9"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>
  <radialGradient id="m"><stop offset="0" stop-color="{moon}" stop-opacity=".45"/><stop offset="1" stop-color="{moon}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g"><stop offset="0" stop-color="{glow}" stop-opacity=".38"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="{bg}"/>
<circle cx="1050" cy="460" r="120" fill="url(#g)"/>
<circle cx="1818" cy="262" r="60" fill="url(#m)"/>
{strokes(LINE, line, 7)}
{strokes(BOTTLE, accent, 7)}
</svg>'''

out = Path(__file__).parent
(out / "scene-navy.svg").write_text(svg("#230052", "#C9D2FF", "#FC4C02", "#FC4C02", "#FFE7C2"))
(out / "scene-cream.svg").write_text(svg("#F5F2EA", "#230052", "#FC4C02", "#FFB48F", "#C9D2FF"))
print("ok")
