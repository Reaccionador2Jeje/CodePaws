"""True low-resolution pixel-art sprites for the CodePaws terminal."""

from PIL import Image, ImageDraw
from rich.style import Style
from rich.text import Text

SIZE = 32
BACKGROUND = "#172630"
INK = "#182532"


def _light(color, amount=0.30):
    rgb = [int(color[i:i+2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(v + (255-v)*amount):02x}" for v in rgb)


def _sprite(pet, frame, action):
    image = Image.new("RGBA", (SIZE, SIZE), BACKGROUND)
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = pet.color
    hi = _light(c)
    bob = 1 if frame % 6 in (1, 2, 3) and action != "sleep" else 0

    def box(coords, fill, outline=INK, width=1):
        x1,y1,x2,y2 = coords
        d.rectangle((x1,y1+bob,x2,y2+bob), fill=fill, outline=outline, width=width)
    def oval(coords, fill, outline=INK, width=1):
        x1,y1,x2,y2 = coords
        d.ellipse((x1,y1+bob,x2,y2+bob), fill=fill, outline=outline, width=width)
    def polygon(points, fill, outline=INK):
        d.polygon([(x,y+bob) for x,y in points], fill=fill, outline=outline)

    pid = pet.pet_id
    if pid == "python":
        polygon([(4,25),(5,19),(9,19),(9,14),(13,14),(13,9),(18,7),(25,9),(28,14),(26,20),(21,22),(17,20),(15,25),(9,28)], c)
        box((19,9,25,12), hi)
        oval((22,13,25,16), "#ffffff")
        d.point((24,14+bob), fill=INK)
        d.line((6,24+bob,3,27+bob), fill=hi, width=2)
    elif pid == "rust":
        polygon([(8,13),(12,9),(20,9),(24,13),(24,21),(19,24),(12,24),(8,21)], c)
        polygon([(8,14),(4,10),(2,12),(4,18),(8,19)], hi)
        polygon([(24,14),(28,10),(30,12),(28,18),(24,19)], hi)
        for x in (9,14,19,23):
            d.line((x,21+bob,x-2,26+bob), fill=INK, width=2)
        oval((12,14,14,17), "#ffffff"); oval((19,14,21,17), "#ffffff")
        d.point((13,15+bob),fill=INK); d.point((20,15+bob),fill=INK)
    elif pid == "go":
        oval((7,8,25,27), c)
        oval((7,4,14,12), hi); oval((18,4,25,12), hi)
        oval((10,15,15,20), "#ffffff"); oval((18,15,23,20), "#ffffff")
        d.point((13,17+bob),fill=INK); d.point((20,17+bob),fill=INK)
        oval((14,21,18,24), "#f2a6a0")
    elif pid == "docker":
        polygon([(3,18),(7,13),(24,13),(28,17),(29,22),(25,26),(9,26),(4,23)], c)
        polygon([(3,18),(1,14),(1,21),(5,24)], hi)
        for x in (8,13,18):
            box((x,8,x+4,13), hi)
        oval((22,17,25,20), "#ffffff"); d.point((24,18+bob),fill=INK)
        polygon([(12,25),(16,29),(20,25)], "#8bd5ff")
    elif pid in ("github","gitlab","kotlin"):
        polygon([(7,13),(6,4),(13,9),(19,9),(26,4),(25,14),(25,22),(20,27),(12,27),(7,22)], c)
        if pid == "gitlab":
            polygon([(7,16),(11,13),(15,16),(20,13),(25,16),(22,22),(10,22)], "#e8d6c1")
        else:
            polygon([(8,14),(12,11),(20,11),(24,14),(22,22),(10,22)], hi)
        box((11,15,13,17), "#ffffff"); box((19,15,21,17), "#ffffff")
        d.point((12,16+bob),fill=INK); d.point((20,16+bob),fill=INK)
        if pid == "github":
            d.line((8,24+bob,5,28+bob,9,28+bob),fill=c,width=3)
    elif pid == "php":
        oval((7,8,25,25), c)
        oval((2,13,12,22), hi); oval((20,13,30,22), hi)
        polygon([(20,18),(25,20),(25,27),(22,30),(19,27)], c)
        oval((11,14,14,17), "#ffffff"); oval((19,14,22,17), "#ffffff")
        d.point((13,15+bob),fill=INK); d.point((20,15+bob),fill=INK)
    elif pid in ("javascript","typescript","ruby"):
        if pid == "javascript":
            box((6,6,26,26), "#f7df1e", "#d19d24", 2)
            box((11,11,14,14), "#ffffff", "#ffffff")
            box((18,18,22,23), INK, INK)
        else:
            polygon([(16,3),(25,10),(27,20),(16,29),(5,20),(7,10)], c)
            polygon([(16,3),(16,29),(5,20),(7,10)], hi)
            polygon([(16,3),(25,10),(16,15)], "#ffffff")
            if pid == "ruby":
                box((12,17,14,19), "#ffffff"); box((19,17,21,19), "#ffffff")
    elif pid in ("c","cpp"):
        box((8,9,24,24), c)
        box((12,4,20,8), hi)
        d.line((16,4+bob,16,1+bob),fill=hi,width=2)
        oval((11,13,15,17), "#ffffff"); oval((18,13,22,17), "#ffffff")
        d.point((13,15+bob),fill=INK); d.point((20,15+bob),fill=INK)
        box((13,20,19,21), "#ffffff")
        if pid == "cpp":
            oval((2,13,8,19), hi); oval((24,13,30,19), hi)
    elif pid == "swift":
        polygon([(5,21),(10,9),(17,5),(26,9),(28,18),(20,24),(11,25)], c)
        polygon([(9,18),(17,13),(24,16),(18,21)], hi)
        polygon([(7,20),(2,25),(12,24)], "#f4d58d")
        oval((20,11,23,14), "#ffffff"); d.point((22,12+bob),fill=INK)
    elif pid == "perl":
        oval((5,18,25,26), c)
        polygon([(19,20),(19,11),(22,6),(26,8),(24,21)], c)
        oval((20,4,27,11), hi)
        polygon([(8,20),(10,13),(14,13),(16,20)], c)
        polygon([(15,20),(18,12),(22,13),(23,20)], c)
        d.point((25,7+bob),fill=INK)
        d.line((9,24+bob,8,29+bob),fill=INK,width=2)
        d.line((21,24+bob,22,29+bob),fill=INK,width=2)
    else:
        # Java and future additions: rounded mascot with a unique color.
        oval((7,6,25,26), c)
        oval((10,9,22,18), hi)
        oval((11,15,14,18), "#ffffff"); oval((19,15,22,18), "#ffffff")
        d.point((13,16+bob),fill=INK); d.point((20,16+bob),fill=INK)

    blink = frame % 30 in (0,1)
    if blink and pid not in ("javascript","typescript","ruby","docker","rust"):
        d.line((11,17+bob,14,17+bob),fill=INK,width=2)
        d.line((18,17+bob,21,17+bob),fill=INK,width=2)
    if action == "sleep":
        d.line((11,17+bob,14,17+bob),fill=INK,width=2)
        d.line((18,17+bob,21,17+bob),fill=INK,width=2)
        d.text((25,1),"z",fill="#8bd5ff")
    elif action == "play":
        d.point((4,5+bob),fill="#f4d58d"); d.point((28,6+bob),fill="#f4d58d")
        d.point((4,27+bob),fill="#f4d58d")
    elif action == "bath":
        d.ellipse((2,5+bob,6,9+bob),outline="#8bd5ff")
        d.ellipse((26,4+bob,30,8+bob),outline="#8bd5ff")

    image.alpha_composite(layer)
    return image.convert("RGB")


def render_pet(pet, frame=0, action=None):
    """Render 32x32 pixel art using two terminal pixels per character."""
    image = _sprite(pet, frame, action)
    result = Text()
    for y in range(0, SIZE, 2):
        for x in range(SIZE):
            top = image.getpixel((x,y))
            bottom = image.getpixel((x,y+1))
            fg = "#{:02x}{:02x}{:02x}".format(*top)
            bg = "#{:02x}{:02x}{:02x}".format(*bottom)
            result.append("▀", Style(color=fg, bgcolor=bg))
        if y < SIZE-2:
            result.append("\n")
    return result
