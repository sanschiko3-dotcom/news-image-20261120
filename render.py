from functools import lru_cache
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER, INK, RED, NAVY = "#f8f4e8", "#111111", "#a3121b", "#1b3a5c"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
OUTPUT = Path(__file__).resolve().parent / "assets" / "entry.png"
LEFT, RIGHT = 28, 996
image = Image.new("RGB", (SIZE, SIZE), PAPER)
draw = ImageDraw.Draw(image)
occupied = []


@lru_cache
def font(size, serif):
    name = "DejaVuSerif-Bold.ttf" if serif else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR / name, size)


def reserve(box, label):
    x, y, right, bottom = box
    assert 0 <= x < right <= SIZE and 0 <= y < bottom <= SIZE, (label, box)
    for (a, b, c, d), other in occupied:
        assert not (x < c and a < right and y < d and b < bottom), (label, other)
    occupied.append((box, label))


def wrap(words, face, width):
    """Yield lines using the available width at each line index."""
    line = ""
    row = 0
    for word in words.split(" "):
        trial = f"{line} {word}" if line else word
        left, _, right, _ = face.getbbox(trial)
        if line and right - left > width(row):
            yield line
            row += 1
            line = word
        else:
            line = trial
    if line:
        yield line


def text(copy, box, size, *, serif=False, color=INK, leading=None,
         align="left", inset=None):
    x, y, right, bottom = box
    face = font(size, serif)
    step = leading or size + 2
    # Keep the baseline consistent, even for lines without descenders.
    top = face.getbbox("H")[1] - 2

    def edge(row):
        line_y = y + row * step
        if inset and line_y < inset[1] and line_y + step > inset[0]:
            return inset[2]
        return right

    end = y
    for row, line in enumerate(wrap(copy, face, lambda i: edge(i) - x)):
        left, upper, far, lower = face.getbbox(line)
        line_y = y + row * step - top
        line_x = x - left if align == "left" else edge(row) - far
        bounds = (line_x + left, line_y + upper, line_x + far, line_y + lower)
        assert x <= bounds[0] and y <= bounds[1], (copy, bounds, box)
        assert bounds[2] <= edge(row) and bounds[3] <= bottom, (copy, bounds, box)
        reserve(bounds, line)
        draw.text((line_x, line_y), line, font=face, fill=color)
        end = bounds[3]
    return end


def rule(y, color=INK, width=1):
    draw.rectangle((LEFT, y, RIGHT - 1, y + width - 1), fill=color)


def star(cx, cy, radius, color, angle=-pi / 2):
    points = []
    for i in range(10):
        r = radius if i % 2 == 0 else radius * 0.382
        theta = angle + i * pi / 5
        points.append((cx + r * cos(theta), cy + r * sin(theta)))
    draw.polygon(points, fill=color)


def bands(x, y, width, height, colors):
    for i, color in enumerate(colors):
        top = y + i * height // len(colors)
        bottom = y + (i + 1) * height // len(colors)
        draw.rectangle((x, top, x + width - 1, bottom - 1), fill=color)


def flag_band(y):
    width, height = 316, 53
    us, china, russia = LEFT, LEFT + 326, LEFT + 652
    reserve((LEFT, y, RIGHT, y + height), "flags")
    white = "#ffffff"
    bands(us, y, width, height, [RED, white] * 6 + [RED])
    canton = height * 7 // 13
    draw.rectangle((us, y, us + 128, y + canton - 1), fill=NAVY)
    for row in range(9):
        for col in range(6 - row % 2):
            star(us + 14 + 20 * col + 10 * (row % 2),
                 y + (row + 1) * canton / 10, 2.6, white)

    bands(china, y, width, height, [RED])
    gold = "#ffd34a"
    star(china + 27, y + 22, 13, gold)
    for dx, dy, angle in [(47, 9, 2.55), (56, 17, 2.97),
                          (56, 30, 3.41), (47, 39, 3.85)]:
        star(china + dx, y + dy, 4.5, gold, angle)
    bands(russia, y, width, height, [white, "#244c99", RED])


def skyline(base):
    reserve((LEFT, base - 41, RIGHT, base + 1), "skyline")
    # A single street line, with low blocks around two taller towers.
    buildings = [
        (0, 31, 8), (25, 37, 15), (70, 44, 10), (110, 34, 19),
        (144, 29, 12), (182, 46, 24), (219, 32, 15), (254, 44, 12),
        (299, 38, 29), (337, 33, 17), (378, 45, 11), (417, 36, 21),
        (451, 26, 14), (482, 48, 9), (526, 37, 16), (566, 43, 25),
        (610, 27, 12), (637, 39, 18), (680, 36, 33), (716, 29, 16),
        (749, 43, 11), (788, 42, 20), (837, 37, 13), (872, 30, 23),
        (906, 34, 15), (938, 30, 9),
    ]
    for offset, width, height in buildings:
        x = LEFT + offset
        draw.rectangle((x, base - height, x + width - 1, base), fill=NAVY)
    for offset, height in [(299, 29), (680, 33)]:
        x = LEFT + offset
        draw.rectangle((x + 8, base - height - 4, x + 27, base - height), fill=NAVY)
        draw.line((x + 18, base - height - 8, x + 18, base - height), fill=NAVY)
    draw.rectangle((LEFT, base - 3, RIGHT - 1, base), fill=NAVY)
    for dx, dy in [(121, 13), (194, 17), (207, 17), (311, 22), (324, 22),
                   (311, 14), (430, 15), (583, 18), (689, 25), (704, 25),
                   (704, 17), (803, 13), (884, 16)]:
        draw.rectangle((LEFT + dx, base - dy, LEFT + dx + 3, base - dy + 2),
                       fill="#dfc58c")


def cyclone(x, y):
    reserve((x, y, x + 90, y + 90), "cyclone")
    # Two tapered spiral arms curl around a clear eye.
    for phase in (0, pi):
        edges = ([], [])
        for i in range(81):
            t = i / 80
            angle = phase + 4.5 * t
            radius = 8 + 34 * t
            thickness = 1 + 7 * sin(pi * t)
            for edge, r in zip(edges, (radius - thickness, radius + thickness)):
                edge.append((x + 45 + r * cos(angle), y + 45 + r * sin(angle)))
        draw.polygon(edges[0] + edges[1][::-1], fill=NAVY)


def article(x, y, right, bottom, kicker, headline, body, *, inset=None):
    text(kicker, (x, y, right, y + 16), 15, serif=True, color=RED)
    end = text(headline, (x, y + 20, right, bottom), 25, serif=True, leading=26)
    text(body, (x, end + 6, right, bottom), 19, leading=19, inset=inset)


def render():
    text("THE WORLD TODAY", (LEFT, 17, RIGHT, 74), 64, serif=True)
    rule(76, width=2)
    text("FRIDAY, 20 NOVEMBER 2026", (LEFT, 85, 470, 103), 16, serif=True)
    text("THE WORLD'S NEWS IN ONE PAGE", (550, 85, RIGHT, 103), 16, align="right")
    rule(106, RED, 2)

    text("SHENZHEN SUMMIT", (LEFT, 116, RIGHT, 131), 16, serif=True, color=RED)
    text("TRUMP, XI AND PUTIN MEET — AND SIGN A JOINT PEACE PLEDGE",
         (LEFT, 137, RIGHT, 215), 38, serif=True, leading=39)
    text("First-ever three-way meeting in Shenzhen brings a joint declaration "
         "committing to peace and stability. Germany's Chancellor Friedrich Merz "
         "warns Europe will accept no new Yalta. An EU-UK summit meets in Brussels "
         "the same day.", (LEFT, 218, RIGHT, 279), 19, leading=20)
    flag_band(282)
    skyline(376)
    rule(380, width=2)

    article(LEFT, 389, 503, 622, "WAR IN UKRAINE",
            "RUSSIA'S BIGGEST BARRAGE HITS KYIV — AND SPILLS INTO POLAND",
            "400+ drones and 110 missiles: 8 killed, about 30 injured. Kyiv bridges "
            "and power grid hit. Two Russian missiles land in Poland's Lublin and "
            "Subcarpathian regions; no casualties. Ukraine hits Kerch Bridge and retakes "
            "14 settlements near Kharkiv: Operation Bear Trap, about 200\u00a0sq\u00a0km.")
    article(521, 389, RIGHT, 622, "THE HAGUE",
            "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
            "The International Court of Justice finds Myanmar committed genocide "
            "against the Rohingya in a landmark ruling. The UN chief welcomes the "
            "ruling and demands accountability.")
    rule(625)
    cyclone(413, 744)
    article(LEFT, 629, 503, 865, "INDIA",
            "CYCLONE AKVAN SLAMS INTO INDIA'S EAST COAST",
            "Landfall near Gopalpur, Odisha, Friday morning. Winds 70-80 km/h, "
            "gusting to 90. More than 300,000 evacuated; 423 rescue teams; 69 trains "
            "cancelled. No major damage or loss of life reported.",
            inset=(744, 834, 400))
    article(521, 629, RIGHT, 865, "THE GULF",
            "TRUMP PUTS IRAN DECISION OFF TO 2027 AS MISSILES FLY OVER RIYADH",
            'New Iran strikes decision deferred until after 1 January 2027: "I\'m not '
            'rushing"; "We\'ve got time". US blockade in Strait of Hormuz. Three Houthi '
            "missiles intercepted late Friday. A strike damages skyscraper floors in "
            "Riyadh's King Abdullah Financial District; no injuries. Saudi-led forces "
            "strike Hodeidah port, Yemen.")
    draw.line((512, 389, 512, 865), fill=NAVY)
    rule(868, width=2)

    text("ALSO TODAY", (LEFT, 873, RIGHT, 890), 16, serif=True, color=RED)
    items = [
        ("COP31 ANTALYA", "Talks run past Friday deadline. Draft drops all fossil-fuel "
         "mention; about 200 countries split."),
        ("ANTHROPIC IPO", "Day two: -8.5% to $88.91 after record $81.3bn IPO. "
         "Nov. 19 debut: +17% to $97.17."),
        ("GTA VI RECORD", "Rockstar: $3.79bn in first-day sales, an entertainment "
         "record after a 13-year wait."),
        ("FRIDAY MARKETS", "Nasdaq -5.28%; S&P\u00a0500 -3.70%; Bitcoin $58,939 (-4.79%); "
         "WTI $83.62 (+0.49%)."),
        ("ENERGY SHIFT", "IEA: the world now needs more energy for cooling than for "
         "heating, for the first time."),
    ]
    column = 192
    for i, (headline, body) in enumerate(items):
        x = LEFT + 4 + i * column
        if i:
            draw.line((x - 5, 892, x - 5, 990), fill=NAVY)
        text(headline, (x, 892, x + 182, 909), 15, serif=True)
        text(body, (x, 911, x + 182, 993), 15, leading=16)

    rule(994)
    text("FRIDAY 20 NOVEMBER 2026 • Sources: Reuters, AP, IMD, UN",
         (LEFT, 1001, RIGHT, 1017), 14)
    image.save(OUTPUT, optimize=True)
    with Image.open(OUTPUT) as png:
        assert png.format == "PNG" and png.size == (SIZE, SIZE)
        png.verify()
    size = OUTPUT.stat().st_size
    assert size < 1024**2, size
    print(f"{OUTPUT.name}: {SIZE}x{SIZE}, {size:,} bytes")


if __name__ == "__main__":
    render()
