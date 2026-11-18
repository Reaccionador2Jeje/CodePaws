"""Hand-crafted, animated pixel-art mascots for CodePaws.

Sprites are drawn on a 48x48 logical pixel canvas and rendered with
Unicode half-blocks so each terminal character carries two colored pixels.
"""

from __future__ import annotations

from PIL import Image, ImageDraw
from rich.style import Style
from rich.text import Text

SIZE = 48
BACKGROUND = "#172630"
INK = "#17212b"
WHITE = "#fff4dc"
SHADOW = "#000000"


def _shade(color: str, factor: float) -> str:
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{max(0, min(255, round(v * factor))):02x}" for v in rgb)


def _draw(pet, frame: int, action: str | None) -> Image.Image:
    image = Image.new("RGB", (SIZE, SIZE), BACKGROUND)
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = pet.color
    hi, mid, dark = _shade(c, 1.25), _shade(c, .82), _shade(c, .55)
    bob = 1 if action != "sleep" and frame % 8 in (1, 2, 3, 4) else 0
    walk = (frame // 3) % 2

    def poly(points, fill, outline=INK, width=2):
        d.polygon([(x, y + bob) for x, y in points], fill=fill, outline=outline, width=width)
    def rect(box, fill, outline=INK, width=2):
        x1,y1,x2,y2=box
        d.rectangle((x1,y1+bob,x2,y2+bob), fill=fill, outline=outline, width=width)
    def oval(box, fill, outline=INK, width=2):
        x1,y1,x2,y2=box
        d.ellipse((x1,y1+bob,x2,y2+bob), fill=fill, outline=outline, width=width)
    def line(points, fill=INK, width=2):
        d.line([(x,y+bob) for x,y in points], fill=fill, width=width)
    def eye(x, y, sleepy=False):
        if sleepy:
            line([(x-2,y),(x+3,y)], INK, 3)
        else:
            oval((x-3,y-4,x+3,y+4), WHITE, INK, 1)
            d.point((x+1,y+bob), fill=INK)
            d.point((x,y-2+bob), fill="#ffffff")
    def smile(x1,y1,x2,y2):
        d.arc((x1,y1+bob,x2,y2+bob), 5, 165, fill=INK, width=2)

    pid = pet.pet_id
    sleepy = action == "sleep" or frame % 36 in (0, 1)

    # Ground shadow makes the character feel anchored in the scene.
    d.ellipse((7, 42, 41, 46), fill=(5, 10, 15, 110))

    if pid == "rust":
        # Ferris: broad red crab, raised animated claws, segmented legs.
        claw_lift = 3 if walk else 0
        poly([(10,20),(13,14),(20,11),(29,11),(36,15),(39,22),(36,31),(29,36),(17,35),(10,29)], c)
        poly([(12,22),(16,16),(22,14),(29,14),(35,19),(35,27),(29,32),(18,32),(13,28)], hi, width=1)
        # Left and right arms, with claws opening and closing.
        line([(12,24),(8,22),(6,17-claw_lift),(3,14-claw_lift)], dark, 5)
        poly([(5,17-claw_lift),(2,13-claw_lift),(3,8-claw_lift),(7,11-claw_lift),(9,7-claw_lift),(11,12-claw_lift),(10,18-claw_lift)], c)
        line([(36,24),(40,21),(42,16+claw_lift),(45,13+claw_lift)], dark, 5)
        poly([(43,16+claw_lift),(41,11+claw_lift),(43,7+claw_lift),(46,11+claw_lift),(47,16+claw_lift),(44,20+claw_lift)], c)
        # Four articulated legs on each side.
        for i, x in enumerate((15,20,27,32)):
            offset = 2 if (i + walk) % 2 else 0
            line([(x,32),(x-3-offset,37),(x-5-offset,40)], dark, 3)
            line([(x+1,33),(x+3+offset,37),(x+5+offset,40)], c, 2)
        eye(20,23,sleepy); eye(29,23,sleepy)
        smile(21,25,29,30)
        # Shell glints.
        line([(17,17),(22,15),(26,15)], "#ffb0a1", 2)
    elif pid == "python":
        # Py: curled snake with a raised head and patterned belly.
        line([(8,37),(5,33),(7,29),(15,29),(20,34),(29,34),(35,29),(35,24)], dark, 9)
        line([(8,36),(6,32),(9,30),(15,31),(21,36),(30,36),(37,30)], c, 6)
        poly([(28,25),(29,17),(33,11),(40,9),(45,12),(46,18),(43,23),(38,26),(33,25)], c)
        poly([(32,16),(35,11),(41,11),(44,14),(42,18),(36,19)], hi, width=1)
        eye(39,16,sleepy)
        d.line([(43,21+bob),(47,22+bob)], fill="#ed7890", width=2)
        for x in (12,18,24,30):
            line([(x,32),(x+2,34)], hi, 2)
        line([(10,30),(7,27)], hi, 2)
    elif pid == "go":
        # Gopher: round blue gopher, big ears and two front teeth.
        oval((10,10,38,41), c)
        oval((8,5,19,19), hi); oval((29,5,40,19), hi)
        oval((12,14,36,37), mid, width=1)
        eye(20,22,sleepy); eye(30,22,sleepy)
        oval((22,27,28,32), "#eaa3a3", INK, 1)
        rect((22,32,25,36), WHITE, INK, 1); rect((26,32,29,36), WHITE, INK, 1)
        oval((7,28,13,35), hi); oval((35,28,41,35), hi)
        line([(17,40),(16,44)], INK, 3); line([(32,40),(33,44)], INK, 3)
    elif pid == "docker":
        # Moby: whale with container stack on its back and tail fin.
        poly([(5,25),(10,19),(35,19),(41,24),(43,32),(38,39),(16,40),(8,35)], c)
        poly([(7,25),(13,21),(35,21),(39,26),(39,32),(34,36),(17,36),(10,32)], hi, width=1)
        poly([(7,27),(2,22),(3,32),(10,36)], dark)
        for x in (13,20,27):
            rect((x,12,x+6,20), hi)
            line([(x+2,14),(x+4,14)], WHITE, 1)
        oval((34,25,38,29), WHITE, INK, 1)
        d.point((37,27+bob), fill=INK)
        poly([(21,37),(26,43),(31,37)], "#8bd5ff")
        line([(14,39),(12,43)], dark, 2); line([(34,39),(36,43)], dark, 2)
    elif pid in ("github","gitlab","kotlin"):
        # Cat-like mascots with pointed ears, cheek patches and tail.
        poly([(9,18),(8,5),(19,12),(29,12),(40,5),(39,19),(38,34),(31,41),(17,41),(10,34)], c)
        poly([(12,19),(14,14),(20,15),(28,15),(35,19),(34,31),(29,36),(18,36),(13,31)], hi, width=1)
        if pid == "gitlab":
            poly([(12,22),(18,18),(23,22),(29,18),(35,22),(32,30),(16,30)], "#f1dfc8", width=1)
            eye(19,24,sleepy); eye(29,24,sleepy)
        else:
            eye(19,24,sleepy); eye(30,24,sleepy)
            oval((22,29,27,33), "#f29aaa", INK, 1)
        smile(21,29,29,35)
        if pid == "github":
            line([(12,36),(7,40),(4,38)], c, 4)
        elif pid == "kotlin":
            line([(36,35),(42,39),(44,36)], hi, 3)
    elif pid == "php":
        # ElePHPant: elephant with floppy ears and a curved trunk.
        oval((11,11,38,39), c)
        oval((3,17,17,33), hi); oval((33,17,46,33), hi)
        poly([(31,27),(37,29),(38,36),(34,42),(29,39),(30,34)], c)
        eye(21,23,sleepy); eye(31,23,sleepy)
        line([(22,33),(29,34)], INK, 2)
        line([(17,38),(16,43)], dark, 3); line([(34,38),(35,43)], dark, 3)
    elif pid == "javascript":
        # Javie: expressive yellow square sprite with tiny arms and feet.
        rect((8,8,40,39), "#f7df1e", "#c49c16", 3)
        rect((12,12,36,35), "#ffe94f", "#e1b91b", 1)
        eye(19,22,sleepy); eye(30,22,sleepy)
        smile(20,25,30,32)
        line([(8,25),(3,29)], c, 4); line([(40,25),(45,29)], c, 4)
        line([(17,39),(14,44)], dark, 3); line([(32,39),(35,44)], dark, 3)
    elif pid in ("typescript","ruby"):
        # Faceted crystal creatures with layered highlights.
        poly([(24,4),(39,15),(42,30),(24,44),(6,30),(9,15)], c, width=3)
        poly([(24,7),(36,16),(24,23),(12,16)], hi, width=1)
        poly([(12,18),(24,25),(24,40),(8,29)], mid, width=1)
        poly([(36,18),(24,25),(24,40),(40,29)], dark, width=1)
        eye(19,26,sleepy); eye(29,26,sleepy)
        line([(21,33),(27,33)], INK, 2)
        if pid == "ruby":
            poly([(24,5),(29,11),(24,15),(19,11)], "#ffd5dd", width=1)
    elif pid in ("c","cpp"):
        # Cee and PlusPlus: chunky little robots with antennae.
        line([(24,8),(24,3)], hi, 3); oval((21,1,27,7), "#f4d58d")
        rect((8,11,40,38), c, dark, 3)
        rect((12,15,36,33), hi, width=1)
        eye(19,23,sleepy); eye(30,23,sleepy)
        rect((19,31,29,34), INK, INK, 1)
        line([(8,23),(3,27)], dark, 4); line([(40,23),(45,27)], dark, 4)
        line([(16,38),(14,44)], dark, 4); line([(33,38),(35,44)], dark, 4)
        if pid == "cpp":
            oval((2,17,10,25), "#d8e8f8"); oval((38,17,46,25), "#d8e8f8")
    elif pid == "swift":
        # Swiftie: bright bird with wings and beak.
        poly([(6,29),(10,17),(20,9),(34,12),(42,23),(37,34),(25,40),(13,37)], c)
        poly([(12,28),(20,18),(34,19),(27,32),(17,35)], hi)
        poly([(39,22),(47,25),(39,29)], "#f4d58d")
        eye(34,20,sleepy)
        poly([(9,29),(2,37),(16,35)], dark)
        line([(22,39),(20,44)], INK, 3); line([(30,39),(32,44)], INK, 3)
    elif pid == "perl":
        # Camel with twin humps and a tall neck.
        oval((5,25,35,39), c)
        poly([(27,31),(29,15),(34,9),(39,11),(38,31)], c)
        oval((34,6,43,15), hi)
        poly([(9,29),(11,18),(17,17),(21,29)], c)
        poly([(19,29),(23,17),(29,18),(31,30)], c)
        eye(40,10,sleepy)
        line([(12,37),(10,44)], dark, 4); line([(30,37),(32,44)], dark, 4)
    else:
        # Duke and future catalog additions: custom-colored friendly mascot.
        oval((9,7,39,41), c)
        oval((13,11,35,25), hi, width=1)
        eye(20,24,sleepy); eye(30,24,sleepy)
        smile(20,26,31,34)
        line([(16,39),(14,44)], dark, 3); line([(32,39),(34,44)], dark, 3)

    # Action overlays are deliberately separate from the base character art.
    if action == "sleep":
        d.text((37,2), "Z", fill="#8bd5ff")
        d.text((42,8), "z", fill="#8bd5ff")
    elif action == "play":
        d.point((5,7), fill="#ffe08a"); d.point((43,8), fill="#ffe08a")
        d.point((5,40), fill="#ffe08a"); d.point((43,39), fill="#ffe08a")
    elif action == "bath":
        d.ellipse((3,5,8,10), outline="#8bd5ff", width=2)
        d.ellipse((40,4,46,10), outline="#8bd5ff", width=2)
        d.point((8,15), fill="#ffffff"); d.point((39,14), fill="#ffffff")

    image.alpha_composite(layer)
    return image


def render_pet(pet, frame=0, action=None):
    """Render detailed 48x48 pixel art in terminal true-color half-blocks."""
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
            output.append("\n")
    return output
