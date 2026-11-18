"""Reference-informed, friendly pixel-art companions for CodePaws.

The sprites are original small-scale interpretations of the visual references
listed in docs/mascot-references.md. They are not copied source artwork.
"""
from __future__ import annotations

from PIL import Image, ImageDraw
from rich.style import Style
from rich.text import Text

SIZE = 48
BACKGROUND = "#172630"
INK = "#17212b"
WHITE = "#fff7e8"


def _shade(color: str, factor: float) -> str:
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{max(0, min(255, round(v * factor))):02x}" for v in rgb)


def _draw(pet, frame: int, action: str | None) -> Image.Image:
    image = Image.new("RGBA", (SIZE, SIZE), BACKGROUND)
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pid = pet.pet_id
    c = pet.color
    hi, mid, dark = _shade(c, 1.22), _shade(c, .82), _shade(c, .56)
    bob = 1 if action != "sleep" and frame % 8 in (1, 2, 3, 4) else 0
    step = (frame // 3) % 2
    sleepy = action == "sleep" or frame % 42 in (0, 1)

    def oval(box, fill, outline=INK, width=2):
        x1, y1, x2, y2 = box
        d.ellipse((x1, y1 + bob, x2, y2 + bob), fill=fill, outline=outline, width=width)

    def rect(box, fill, outline=INK, width=2, radius=2):
        x1, y1, x2, y2 = box
        d.rounded_rectangle((x1, y1 + bob, x2, y2 + bob), radius=radius,
                            fill=fill, outline=outline, width=width)

    def poly(points, fill, outline=INK, width=2):
        d.polygon([(x, y + bob) for x, y in points], fill=fill, outline=outline, width=width)

    def line(points, fill=INK, width=2):
        d.line([(x, y + bob) for x, y in points], fill=fill, width=width, joint="curve")

    def eye(x, y, closed=False, color=WHITE):
        if closed or sleepy:
            line([(x - 2, y), (x + 2, y)], INK, 2)
        else:
            oval((x - 2, y - 3, x + 2, y + 3), color, INK, 1)
            d.point((x + 1, y + bob), fill=INK)

    def smile(box=(20, 27, 29, 33)):
        d.arc((box[0], box[1] + bob, box[2], box[3] + bob),
              5, 165, fill=INK, width=2)

    d.ellipse((7, 43, 41, 47), fill=(4, 9, 13, 115))

    if pid == "python":
        # Python's blue/yellow interlocking snake mark, adapted into two heads.
        line([(9, 32), (9, 25), (14, 21), (21, 21), (25, 25), (25, 30),
              (30, 34), (37, 34)], "#ffd343", 8)
        line([(9, 32), (9, 25), (14, 21), (21, 21), (25, 25), (25, 30),
              (30, 34), (37, 34)], "#ffd343", 5)
        line([(39, 16), (39, 23), (34, 27), (27, 27), (23, 23), (23, 18),
              (18, 14), (11, 14)], "#4584b6", 8)
        line([(39, 16), (39, 23), (34, 27), (27, 27), (23, 23), (23, 18),
              (18, 14), (11, 14)], "#4584b6", 5)
        rect((5, 8, 21, 19), "#4584b6", "#244e70", 2, 4)
        rect((27, 29, 43, 40), "#ffd343", "#9b7822", 2, 4)
        oval((9, 11, 12, 14), WHITE, INK, 1)
        oval((31, 32, 34, 35), WHITE, INK, 1)
        d.point((11, 12 + bob), fill=INK)
        d.point((33, 33 + bob), fill=INK)

    elif pid == "rust":
        # Ferris: orange crab with a broad spiky shell and raised pincers.
        oval((10, 17, 38, 37), "#f05a28")
        poly([(11, 24), (9, 16), (13, 18), (15, 10), (20, 15),
              (24, 7), (28, 15), (34, 10), (34, 19), (39, 17), (37, 27)],
             "#f05a28", "#a63d1f", 2)
        oval((14, 20, 34, 34), "#ff7b43", width=1)
        line([(12, 25), (7, 21), (5, 15)], "#b94725", 4)
        line([(36, 25), (41, 21), (43, 15)], "#b94725", 4)
        poly([(3, 16), (2, 10), (6, 7), (10, 12), (13, 7), (14, 15), (10, 19)], "#f05a28")
        poly([(40, 16), (39, 10), (43, 7), (46, 12), (47, 7), (47, 16), (44, 19)], "#f05a28")
        for x in (14, 20, 27, 33):
            off = 2 if (x // 3 + step) % 2 else 0
            line([(x, 34), (x - 3, 39 + off), (x - 4, 42 + off)], "#b94725", 3)
        eye(20, 25); eye(29, 25); smile((21, 27, 29, 33))
        line([(17, 20), (22, 18), (27, 18)], "#ffbd9f", 2)

    elif pid == "go":
        # Go Gopher: upright blue body, round ears, huge eyes and two teeth.
        oval((9, 12, 39, 43), "#79d2e5", "#244b60", 2)
        oval((4, 5, 20, 22), "#79d2e5", "#244b60", 2)
        oval((28, 5, 44, 22), "#79d2e5", "#244b60", 2)
        oval((8, 12, 17, 20), "#b4e9f1", width=1)
        oval((31, 12, 40, 20), "#b4e9f1", width=1)
        oval((12, 16, 36, 37), "#a5e3ed", width=1)
        oval((13, 19, 23, 30), WHITE, INK, 1)
        oval((25, 19, 35, 30), WHITE, INK, 1)
        d.ellipse((17, 22 + bob, 21, 27 + bob), fill=INK)
        d.ellipse((27, 22 + bob, 31, 27 + bob), fill=INK)
        oval((20, 29, 28, 34), "#d7a17d", INK, 1)
        rect((20, 33, 24, 39), WHITE, INK, 1, 1)
        rect((25, 33, 29, 39), WHITE, INK, 1, 1)
        line([(10, 31), (5, 34), (5, 38)], "#f0c59f", 3)
        line([(38, 31), (43, 34), (43, 38)], "#f0c59f", 3)
        line([(17, 42), (15, 45)], "#f0c59f", 3)
        line([(31, 42), (33, 45)], "#f0c59f", 3)

    elif pid == "java":
        # Duke: white body, pointed dark head, bright red nose and akimbo arms.
        poly([(14, 19), (18, 8), (24, 3), (30, 8), (34, 19),
              (34, 34), (29, 41), (19, 41), (14, 34)], WHITE, INK, 2)
        poly([(17, 19), (19, 8), (24, 2), (29, 8), (32, 19)], "#202027", "#11151b", 2)
        oval((19, 17, 30, 29), "#fffdf7", "#c9c9c9", 1)
        oval((21, 18, 29, 26), "#c8103e", "#72112d", 1)
        oval((23, 19, 26, 22), WHITE, WHITE, 1)
        line([(15, 25), (9, 29), (7, 26)], INK, 4)
        line([(33, 25), (39, 29), (41, 26)], INK, 4)
        line([(19, 39), (16, 44)], INK, 4)
        line([(29, 39), (32, 44)], INK, 4)

    elif pid == "docker":
        # Moby Dock reference: blue whale carrying tiered shipping containers.
        poly([(7, 28), (2, 22), (3, 33), (10, 37)], "#176eae", "#143e5b", 2)
        oval((7, 21, 43, 41), "#2496ed", "#143e5b", 2)
        poly([(10, 31), (18, 34), (34, 34), (40, 29), (37, 38), (17, 40)],
             "#d8f1ff", "#143e5b", 1)
        # stepped container stack with ribbing
        for x, y, w in ((12, 14, 8), (21, 14, 8), (30, 14, 7),
                        (17, 7, 8), (26, 7, 8), (22, 1, 8)):
            rect((x, y, x + w, y + 7), "#43b8ee", "#155783", 1, 0)
            for rx in range(x + 2, x + w - 1, 3):
                line([(rx, y + 1), (rx, y + 6)], "#1673aa", 1)
        eye(35, 28)
        line([(34, 33), (37, 34), (40, 32)], "#143e5b", 1)

    elif pid == "github":
        # Mona/Octocat: cat head, pink face, and soft tentacle-like legs.
        poly([(8, 19), (7, 5), (18, 12), (30, 12), (41, 5),
              (40, 20), (37, 32), (30, 38), (18, 38), (11, 32)],
             "#7654a8", "#39284f", 2)
        oval((12, 16, 36, 34), "#f1b6d0", "#39284f", 1)
        eye(20, 23); eye(29, 23)
        oval((22, 27, 27, 31), "#9a5b79", INK, 1)
        smile((21, 28, 29, 34))
        for pts in (
            [(14, 34), (9, 38), (8, 43), (4, 42)],
            [(20, 37), (18, 41), (20, 45)],
            [(28, 37), (30, 41), (28, 45)],
            [(34, 34), (40, 38), (41, 43), (45, 42)],
        ):
            line(pts, "#7654a8", 4)
        line([(13, 17), (17, 14)], "#b59bd8", 2)
        line([(31, 14), (35, 17)], "#b59bd8", 2)

    elif pid == "gitlab":
        # Tanuki: orange/yellow geometric mask and infinity-loop cheeks.
        poly([(6, 10), (18, 5), (24, 14), (30, 5), (42, 10),
              (39, 25), (24, 42), (9, 25)], "#fc6d26", "#a43d20", 2)
        poly([(9, 13), (18, 9), (24, 19), (30, 9), (39, 13),
              (35, 25), (24, 35), (13, 25)], "#fca326", "#c86a1c", 1)
        poly([(11, 22), (18, 17), (24, 23), (30, 17), (37, 22),
              (33, 29), (24, 34), (15, 29)], "#fff0d5", "#9b542b", 1)
        eye(19, 24); eye(29, 24)
        oval((22, 28, 27, 32), "#75452e", INK, 1)
        smile((21, 29, 29, 35))

    elif pid == "php":
        # ElePHPant: blue elephant, oversized ears and curled trunk.
        oval((11, 13, 39, 41), "#8899ff", "#424d9a", 2)
        oval((2, 16, 20, 34), "#aab7ff", "#424d9a", 2)
        oval((30, 16, 46, 34), "#aab7ff", "#424d9a", 2)
        oval((13, 17, 36, 37), "#9ba9ff", width=1)
        eye(21, 23); eye(30, 23)
        line([(30, 27), (36, 30), (37, 36), (33, 42), (29, 40), (30, 35)],
             "#8899ff", 5)
        line([(17, 39), (15, 44)], "#424d9a", 3)
        line([(34, 39), (36, 44)], "#424d9a", 3)

    elif pid == "javascript":
        # JavaScript identity: yellow square and dark JS monogram.
        rect((6, 6, 42, 42), "#f7df1e", "#9e8514", 1, 1)
        d.text((17, 25 + bob), "JS", fill="#252525", stroke_width=0)
        # Small original companion feet keep the logo-inspired pet lively.
        line([(15, 42), (13, 45)], "#d2a900", 3)
        line([(34, 42), (36, 45)], "#d2a900", 3)

    elif pid == "typescript":
        # TypeScript identity: saturated blue tile and white TS monogram.
        rect((6, 6, 42, 42), "#3178c6", "#1e4d82", 1, 1)
        d.text((12, 21 + bob), "TS", fill="#ffffff", stroke_width=0)
        line([(15, 42), (13, 45)], "#1e4d82", 3)
        line([(34, 42), (36, 45)], "#1e4d82", 3)

    elif pid == "ruby":
        # Ruby's red multifaceted gemstone mark, with a subtle friendly face.
        poly([(7, 15), (15, 7), (33, 7), (41, 15), (37, 31),
              (24, 43), (11, 31)], "#c91432", "#701327", 2)
        poly([(8, 15), (16, 8), (24, 15), (15, 22)], "#ff8290", "#a51b34", 1)
        poly([(16, 8), (32, 8), (40, 15), (24, 22)], "#ed4058", "#a51b34", 1)
        poly([(8, 17), (23, 24), (23, 40), (12, 31)], "#b10f2d", "#7c1429", 1)
        poly([(40, 17), (25, 24), (25, 40), (36, 31)], "#8d1028", "#7c1429", 1)
        eye(19, 27); eye(29, 27); smile((21, 29, 28, 35))

    elif pid == "c":
        # C language mark: white C on a deep-blue hexagon, mascot-sized.
        poly([(15, 5), (33, 5), (44, 15), (44, 33),
              (33, 43), (15, 43), (4, 33), (4, 15)], "#07599f", "#063b68", 2)
        d.text((12, 10 + bob), "C", fill="#ffffff", stroke_width=0)

    elif pid == "cpp":
        # C++ identity: blue hexagonal badge with clear C++ lettering.
        poly([(15, 5), (33, 5), (44, 15), (44, 33),
              (33, 43), (15, 43), (4, 33), (4, 15)], "#659ad2", "#315d8b", 2)
        d.text((8, 11 + bob), "C++", fill="#ffffff", stroke_width=0)

    elif pid == "kotlin":
        # Kodee: purple angular body, black screen face, big white eyes.
        poly([(9, 12), (8, 5), (20, 13), (28, 13), (40, 5),
              (39, 25), (34, 33), (14, 33)], "#8054f6", "#4d2b9b", 2)
        rect((11, 15, 37, 31), "#111016", "#2c1d4c", 2, 4)
        oval((16, 18, 24, 27), WHITE, WHITE, 1)
        oval((26, 18, 34, 27), WHITE, WHITE, 1)
        d.ellipse((19, 20 + bob, 22, 25 + bob), fill="#111016")
        d.ellipse((28, 20 + bob, 31, 25 + bob), fill="#111016")
        smile((21, 25, 29, 30))
        line([(11, 21), (5, 27), (4, 34)], "#8054f6", 4)
        line([(37, 21), (43, 15), (44, 9)], "#8054f6", 4)
        line([(18, 33), (16, 42), (13, 43)], "#8054f6", 5)
        line([(30, 33), (32, 42), (35, 43)], "#8054f6", 5)

    elif pid == "swift":
        # Swift bird emblem interpreted as a compact red-orange flying bird.
        poly([(5, 30), (15, 27), (22, 20), (9, 7), (27, 17),
              (35, 4), (34, 23), (44, 29), (33, 33),
              (24, 41), (13, 39)], "#f05138", "#9d2c22", 2)
        poly([(7, 30), (20, 28), (28, 22), (23, 34), (13, 38)],
             "#ff9b43", "#c24a2b", 1)
        line([(24, 40), (22, 45)], "#9d2c22", 2)
        line([(31, 37), (33, 43)], "#9d2c22", 2)

    elif pid == "perl":
        # Perl camel emblem: white camel silhouette in a deep-blue roundel.
        oval((3, 3, 45, 45), "#075b85", "#063d60", 1)
        poly([(8, 27), (10, 22), (16, 21), (19, 25), (23, 23),
              (28, 25), (32, 31), (35, 34), (41, 34), (42, 38),
              (34, 38), (30, 35), (27, 30), (23, 31), (20, 38),
              (16, 38), (17, 31), (13, 30), (11, 36), (8, 36),
              (9, 30)], WHITE, WHITE, 1)
        poly([(9, 23), (7, 18), (10, 14), (14, 14), (16, 17),
              (14, 22)], WHITE, WHITE, 1)
        line([(10, 17), (8, 15)], WHITE, 1)

    accessory = getattr(pet, "accessory", "none")
    if accessory == "cap":
        d.polygon([(14, 9 + bob), (20, 4 + bob), (31, 5 + bob), (36, 11 + bob)],
                  fill="#e34f65", outline=INK)
        d.rounded_rectangle((11, 10 + bob, 38, 13 + bob), radius=2,
                            fill="#f4d58d", outline=INK)
    elif accessory == "bow":
        d.polygon([(18, 9 + bob), (10, 5 + bob), (11, 14 + bob), (19, 12 + bob)],
                  fill="#ff75b5", outline=INK)
        d.polygon([(20, 9 + bob), (29, 5 + bob), (28, 14 + bob), (20, 12 + bob)],
                  fill="#ff75b5", outline=INK)
        d.ellipse((17, 7 + bob, 22, 12 + bob), fill="#ffe5f1", outline=INK)
    elif accessory == "glasses":
        d.rounded_rectangle((13, 20 + bob, 22, 27 + bob), radius=2,
                            outline="#8bd5ff", width=2)
        d.rounded_rectangle((27, 20 + bob, 36, 27 + bob), radius=2,
                            outline="#8bd5ff", width=2)
        d.line((22, 23 + bob, 27, 23 + bob), fill="#8bd5ff", width=2)
    elif accessory == "crown":
        d.polygon([(12, 13 + bob), (13, 5 + bob), (19, 10 + bob),
                   (24, 2 + bob), (29, 10 + bob), (35, 5 + bob),
                   (36, 13 + bob)], fill="#f4d058", outline=INK)
        d.rectangle((13, 12 + bob, 35, 16 + bob), fill="#e6a92e", outline=INK)
        d.point((24, 7 + bob), fill="#ff6b8a")

    if action == "sleep":
        d.text((38, 2), "Z", fill="#8bd5ff")
        d.text((43, 8), "z", fill="#8bd5ff")
    elif action == "play":
        for x, y in ((5, 7), (43, 8), (5, 40), (43, 39)):
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill="#ffe08a")
    elif action == "bath":
        d.ellipse((3, 5, 8, 10), outline="#8bd5ff", width=2)
        d.ellipse((40, 4, 46, 10), outline="#8bd5ff", width=2)

    image.alpha_composite(layer)
    return image.convert("RGB")


def render_pet(pet, frame=0, action=None):
    """Render reference-informed 48x48 pixel art using terminal true color."""
    image = _draw(pet, frame, action)
    output = Text()
    for y in range(0, SIZE, 2):
        for x in range(SIZE):
            top = image.getpixel((x, y))
            bottom = image.getpixel((x, y + 1))
            foreground = "#{:02x}{:02x}{:02x}".format(*top)
            background = "#{:02x}{:02x}{:02x}".format(*bottom)
            output.append("▀", Style(color=foreground, bgcolor=background))
        if y < SIZE - 2:
            output.append("\\n")
    return output
