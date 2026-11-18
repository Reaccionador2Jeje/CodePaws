"""Friendly, recognizable pixel-art programming mascots for CodePaws.

Each mascot has its own silhouette and details. The designs are fan-made
interpretations; where a technology has no official character, CodePaws
uses an original friendly companion.
"""
from __future__ import annotations

from PIL import Image, ImageDraw
from rich.style import Style
from rich.text import Text

SIZE = 48
BACKGROUND = "#172630"
INK = "#20313b"
WHITE = "#fff7e8"


def _shade(color: str, factor: float) -> str:
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{max(0, min(255, round(v * factor))):02x}" for v in rgb)


def _draw(pet, frame: int, action: str | None) -> Image.Image:
    image = Image.new("RGBA", (SIZE, SIZE), BACKGROUND)
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pid, c = pet.pet_id, pet.color
    hi, mid, dark = _shade(c, 1.22), _shade(c, .82), _shade(c, .56)
    bob = 1 if action != "sleep" and frame % 8 in (1, 2, 3, 4) else 0
    step = (frame // 3) % 2
    sleepy = action == "sleep" or frame % 42 in (0, 1)

    def shift(points):
        return [(x, y + bob) for x, y in points]
    def poly(points, fill, outline=INK, width=2):
        d.polygon(shift(points), fill=fill, outline=outline, width=width)
    def oval(box, fill, outline=INK, width=2):
        x1,y1,x2,y2=box
        d.ellipse((x1,y1+bob,x2,y2+bob), fill=fill, outline=outline, width=width)
    def rect(box, fill, outline=INK, width=2):
        x1,y1,x2,y2=box
        d.rounded_rectangle((x1,y1+bob,x2,y2+bob), radius=2, fill=fill, outline=outline, width=width)
    def line(points, fill=INK, width=2):
        d.line(shift(points), fill=fill, width=width, joint="curve")
    def eye(x, y, closed=False):
        if closed or sleepy:
            line([(x-2,y),(x+2,y)], INK, 2)
        else:
            oval((x-2,y-3,x+2,y+3), WHITE, INK, 1)
            d.point((x+1,y+bob), fill=INK)
    def smile(box=(20,27,29,33)):
        d.arc((box[0],box[1]+bob,box[2],box[3]+bob), 5, 165, fill=INK, width=2)

    d.ellipse((7,43,41,47), fill=(4,9,13,115))

    if pid == "python":
        # Two friendly intertwined Python snakes: blue and golden yellow.
        line([(8,34),(13,38),(21,38),(27,33),(24,28),(17,27),(13,23),(16,18),(23,17),(29,21)], "#ffd343", 8)
        line([(8,34),(13,38),(21,38),(27,33),(24,28),(17,27),(13,23),(16,18),(23,17),(29,21)], "#ffd343", 5)
        line([(40,34),(35,38),(27,38),(21,33),(24,28),(31,27),(35,23),(32,18),(25,17),(19,21)], "#4584b6", 8)
        line([(40,34),(35,38),(27,38),(21,33),(24,28),(31,27),(35,23),(32,18),(25,17),(19,21)], "#4584b6", 5)
        oval((21,7,34,20), "#ffd343"); oval((14,7,27,20), "#4584b6")
        oval((23,11,32,18), "#ffe36c", width=1); oval((16,11,25,18), "#6da7d0", width=1)
        eye(27,13); eye(20,13)
        d.point((31,16+bob), fill=INK); d.point((17,16+bob), fill=INK)
        # Tiny forked tongues.
        line([(33,18),(37,20),(39,18)], "#f28b8b", 1)
        line([(14,18),(10,20),(8,18)], "#f28b8b", 1)

    elif pid == "rust":
        # Ferris, the cheerful orange Rust crab.
        oval((11,16,37,37), c)
        oval((14,18,34,34), hi, width=1)
        line([(12,25),(7,22),(5,16)], dark, 4)
        line([(36,25),(41,22),(43,16)], dark, 4)
        poly([(4,17),(2,12),(5,8),(9,12),(12,8),(13,14),(10,19)], c)
        poly([(42,17),(40,12),(43,8),(46,12),(47,8),(47,16),(44,19)], c)
        for x in (15,21,27,33):
            off=2 if (x//3+step)%2 else 0
            line([(x,34),(x-3,39+off),(x-4,42+off)], dark, 3)
        eye(20,25); eye(29,25); smile((21,27,29,33))
        line([(17,20),(22,18),(27,18)], "#ffb39e", 2)

    elif pid == "go":
        # Go Gopher: round blue body, large ears and two unmistakable teeth.
        oval((9,13,39,42), c)
        oval((5,5,20,21), hi); oval((28,5,43,21), hi)
        oval((10,15,38,39), "#b9e2f5", width=1)
        oval((15,20,33,34), "#e9f5fb", width=1)
        eye(20,24); eye(29,24)
        oval((22,28,27,32), "#d98e9b", INK, 1)
        rect((21,32,25,37), WHITE, INK, 1); rect((26,32,30,37), WHITE, INK, 1)
        oval((6,29,13,36), hi, width=1); oval((35,29,42,36), hi, width=1)
        line([(16,41),(15,44)], dark, 3); line([(32,41),(33,44)], dark, 3)

    elif pid == "java":
        # Duke: white, soft-edged little Java mascot with red nose and blue limbs.
        oval((14,8,34,31), WHITE, "#b8c7d0", 2)
        poly([(17,29),(31,29),(36,39),(12,39)], "#4d8cc9")
        line([(16,33),(8,39),(6,36)], "#4d8cc9", 4)
        line([(32,33),(40,39),(42,36)], "#4d8cc9", 4)
        line([(19,38),(17,44)], "#4d8cc9", 4); line([(29,38),(31,44)], "#4d8cc9", 4)
        eye(21,19); eye(29,19)
        oval((23,22,28,27), "#e94c55", "#b8323b", 1)
        line([(19,13),(24,11),(29,13)], "#d7e0e5", 1)

    elif pid == "docker":
        # Moby: whale body, tail flukes and the familiar container stack.
        poly([(5,25),(10,20),(34,20),(41,24),(44,31),(39,38),(17,40),(8,35)], c)
        poly([(8,26),(13,22),(34,22),(39,26),(40,32),(34,36),(17,37),(10,33)], hi, width=1)
        poly([(8,27),(2,21),(3,32),(11,37)], dark)
        for x,h in ((12,7),(19,10),(26,7),(33,4)):
            rect((x,19-h,x+6,19), "#e9f5fb", "#2d729c", 1)
            line([(x+2,17-h),(x+4,17-h)], "#9bc8df", 1)
        eye(35,27); smile((29,29,37,34))
        poly([(20,38),(25,44),(30,38)], "#8bd5ff", width=1)

    elif pid == "github":
        # Octocat: cat head plus eight curled tentacles.
        poly([(9,20),(8,5),(19,12),(29,12),(40,5),(39,20),(36,32),(29,38),(19,38),(12,32)], c)
        oval((13,16,35,34), hi, width=1)
        eye(20,23); eye(29,23)
        oval((22,27,27,31), "#f4a6b7", INK, 1)
        smile((21,28,29,34))
        for pts in (
            [(15,34),(10,37),(8,42),(4,41)],
            [(19,36),(17,40),(19,44)],
            [(25,37),(25,41),(28,44)],
            [(32,34),(38,37),(40,42),(44,41)],
        ):
            line(pts, c, 4)
        line([(14,17),(18,14)], hi, 2); line([(30,14),(34,17)], hi, 2)

    elif pid == "gitlab":
        # Tanuki: warm orange raccoon with dark eye mask and striped tail.
        oval((10,14,38,40), c)
        oval((4,7,18,24), hi); oval((30,7,44,24), hi)
        oval((13,17,35,35), "#f6d9bd", width=1)
        poly([(12,21),(18,17),(23,21),(28,17),(36,21),(33,28),(25,30),(16,28)], "#46515d", width=1)
        eye(19,23); eye(29,23)
        oval((22,27,27,31), "#3c4650", INK, 1)
        smile((21,29,29,34))
        line([(34,36),(41,40),(45,37)], c, 5)
        line([(39,39),(42,40),(44,38)], WHITE, 2)

    elif pid == "php":
        # ElePHPant: blue elephant with broad ears and a curved trunk.
        oval((11,13,38,40), c)
        oval((3,17,19,34), hi); oval((30,17,46,34), hi)
        oval((13,17,36,36), mid, width=1)
        eye(21,23); eye(30,23)
        line([(29,27),(35,30),(36,36),(32,41),(28,39),(29,34)], c, 5)
        line([(17,39),(16,44)], dark, 3); line([(34,39),(35,44)], dark, 3)
        oval((7,24,12,29), "#a9b9ff", width=1)

    elif pid == "javascript":
        # Javie: bright yellow rounded square, like the JS identity.
        rect((7,7,41,41), "#f7df1e", "#c49c16", 3)
        rect((11,11,37,37), "#ffe94f", "#e1b91b", 1)
        eye(19,22); eye(30,22); smile((20,26,30,33))
        line([(8,27),(3,30)], "#f7df1e", 4); line([(40,27),(45,30)], "#f7df1e", 4)
        line([(17,40),(14,44)], dark, 3); line([(32,40),(35,44)], dark, 3)
        d.text((17,30), "JS", fill="#9c7910")

    elif pid == "typescript":
        # Tessa is an original CodePaws owl companion (TypeScript has no official mascot).
        oval((8,8,40,42), "#3178c6")
        poly([(9,17),(7,6),(20,13),(28,13),(41,6),(39,18)], "#4d91df")
        oval((12,16,36,34), "#d9edff", width=1)
        oval((15,19,23,28), WHITE, "#245b99", 1); oval((25,19,33,28), WHITE, "#245b99", 1)
        d.ellipse((18,21+bob,21,26+bob), fill=INK); d.ellipse((27,21+bob,30,26+bob), fill=INK)
        poly([(21,29),(27,29),(24,34)], "#f4b84d", width=1)
        line([(17,40),(15,44)], "#f4b84d", 3); line([(31,40),(33,44)], "#f4b84d", 3)

    elif pid == "ruby":
        # Ruby: polished red gemstone with facets and a friendly face.
        poly([(8,15),(16,7),(32,7),(40,15),(37,32),(24,43),(11,32)], c, width=3)
        poly([(10,15),(18,9),(30,9),(38,15),(24,22)], "#ff9bad", width=1)
        poly([(10,17),(23,24),(23,39),(12,31)], "#c93657", width=1)
        poly([(38,17),(25,24),(25,39),(36,31)], "#a82e4d", width=1)
        eye(19,27); eye(29,27); smile((21,29,28,35))
        poly([(19,10),(24,5),(29,10),(24,15)], "#ffd2dc", width=1)

    elif pid == "c":
        # Cee: compact friendly robot, an original CodePaws character.
        rect((9,12,39,38), c, dark, 3)
        rect((13,16,35,32), "#e3eaf0", width=1)
        oval((17,20,23,27), "#6ba8d8", INK, 1); oval((26,20,32,27), "#6ba8d8", INK, 1)
        smile((20,26,29,32))
        line([(24,11),(24,5)], dark, 3); oval((20,1,28,8), "#f4d58d")
        line([(9,23),(4,27)], dark, 4); line([(39,23),(44,27)], dark, 4)
        line([(16,38),(14,44)], dark, 4); line([(32,38),(34,44)], dark, 4)

    elif pid == "cpp":
        # PlusPlus: blue gear-bot, another original CodePaws companion.
        oval((7,10,41,42), "#659ad2", dark, 3)
        for x,y in ((24,5),(24,42),(5,26),(43,26),(12,10),(36,10)):
            oval((x-3,y-3,x+3,y+3), "#9bc3ed", dark, 1)
        oval((13,17,35,35), "#dcecff", width=1)
        eye(20,24); eye(29,24); smile((21,27,29,33))
        rect((19,3,29,8), "#dcecff", dark, 1)

    elif pid == "kotlin":
        # Kotlin Koala: rounded grey koala with big fluffy ears.
        oval((10,13,38,41), "#aeb8c5")
        oval((3,5,20,23), "#cbd2dc"); oval((28,5,45,23), "#cbd2dc")
        oval((7,9,16,18), "#e8a9b7", width=1); oval((32,9,41,18), "#e8a9b7", width=1)
        oval((14,17,34,35), "#e5e9ee", width=1)
        eye(20,24); eye(29,24)
        oval((22,26,28,33), "#394958", INK, 1)
        smile((21,30,29,35))
        line([(17,40),(16,44)], dark, 3); line([(32,40),(33,44)], dark, 3)

    elif pid == "swift":
        # Swiftie: friendly orange swift bird with wing, beak and feather crest.
        oval((8,14,40,39), c)
        poly([(12,25),(19,15),(35,17),(29,31),(16,34)], hi)
        poly([(36,20),(47,23),(38,29)], "#f4d58d")
        poly([(14,17),(10,9),(20,14)], dark)
        eye(34,20)
        poly([(9,29),(2,37),(17,35)], dark)
        line([(22,38),(20,44)], INK, 3); line([(30,38),(32,44)], INK, 3)

    elif pid == "perl":
        # Perl camel: two humps, long neck and gentle face.
        oval((5,25,37,40), c)
        oval((8,17,20,31), hi); oval((20,16,32,31), hi)
        poly([(28,31),(29,14),(34,7),(40,9),(41,17),(37,22),(37,33)], c)
        oval((33,6,43,16), hi)
        eye(39,11)
        line([(35,17),(39,18),(42,16)], dark, 2)
        line([(12,38),(10,44)], dark, 4); line([(31,38),(33,44)], dark, 4)
        line([(14,26),(19,24)], "#f4d58d", 2)

    accessory = getattr(pet, "accessory", "none")
    if accessory == "cap":
        d.polygon([(14,9+bob),(20,4+bob),(31,5+bob),(36,11+bob)], fill="#e34f65", outline=INK)
        d.rounded_rectangle((11,10+bob,38,13+bob), radius=2, fill="#f4d58d", outline=INK)
    elif accessory == "bow":
        d.polygon([(18,9+bob),(10,5+bob),(11,14+bob),(19,12+bob)], fill="#ff75b5", outline=INK)
        d.polygon([(20,9+bob),(29,5+bob),(28,14+bob),(20,12+bob)], fill="#ff75b5", outline=INK)
        d.ellipse((17,7+bob,22,12+bob), fill="#ffe5f1", outline=INK)
    elif accessory == "glasses":
        d.rounded_rectangle((13,20+bob,22,27+bob), radius=2, outline="#8bd5ff", width=2)
        d.rounded_rectangle((27,20+bob,36,27+bob), radius=2, outline="#8bd5ff", width=2)
        d.line((22,23+bob,27,23+bob), fill="#8bd5ff", width=2)
    elif accessory == "crown":
        d.polygon([(12,13+bob),(13,5+bob),(19,10+bob),(24,2+bob),(29,10+bob),(35,5+bob),(36,13+bob)], fill="#f4d058", outline=INK)
        d.rectangle((13,12+bob,35,16+bob), fill="#e6a92e", outline=INK)
        d.point((24,7+bob), fill="#ff6b8a")

    if action == "sleep":
        d.text((38,2), "Z", fill="#8bd5ff")
        d.text((43,8), "z", fill="#8bd5ff")
    elif action == "play":
        for x,y in ((5,7),(43,8),(5,40),(43,39)):
            d.ellipse((x-1,y-1,x+1,y+1), fill="#ffe08a")
    elif action == "bath":
        d.ellipse((3,5,8,10), outline="#8bd5ff", width=2)
        d.ellipse((40,4,46,10), outline="#8bd5ff", width=2)

    image.alpha_composite(layer)
    return image.convert("RGB")


def render_pet(pet, frame=0, action=None):
    """Render 48x48 friendly pixel art with terminal true-color half-blocks."""
    image = _draw(pet, frame, action)
    output = Text()
    for y in range(0, SIZE, 2):
        for x in range(SIZE):
            top = image.getpixel((x, y))
            bottom = image.getpixel((x, y + 1))
            fg = "#{:02x}{:02x}{:02x}".format(*top)
            bg = "#{:02x}{:02x}{:02x}".format(*bottom)
            output.append("▀", Style(color=fg, bgcolor=bg))
        if y < SIZE - 2:
            output.append("\n")
    return output
