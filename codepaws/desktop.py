"""CodePaws Desktop: a cozy pixel-art virtual pet game."""

from __future__ import annotations

import random
import sys
import time

import pygame

from .models import create_pet
from .sprites import _draw
from .storage import load_economy, load_family, save_economy, save_family

WIDTH, HEIGHT = 1100, 720
BG = (17, 25, 37)
PANEL = (27, 39, 54)
PANEL_LIGHT = (38, 54, 72)
TEXT = (239, 244, 250)
MUTED = (155, 174, 193)
ACCENT = (117, 220, 180)
ROOMS = [
    ("living", "Living room"),
    ("bedroom", "Bedroom"),
    ("garden", "Garden"),
]


class CodePawsDesktop:
    """Small, self-contained Pygame desktop game."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("CodePaws — Desktop Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("segoeui", 17)
        self.small = pygame.font.SysFont("segoeui", 14)
        self.heading = pygame.font.SysFont("consolas", 25, bold=True)
        self.title = pygame.font.SysFont("consolas", 31, bold=True)
        self.pets, self.selected_pet = load_family()
        if not self.pets:
            self.pets = [create_pet("python")]
            self.selected_pet = "python"
            save_family(self.pets, self.selected_pet)
        self.economy = load_economy()
        self.active_action: str | None = None
        self.action_until = 0.0
        self.frame = 0
        self.last_tick = time.monotonic()
        self.last_save = self.last_tick
        self.running = True
        self.buttons: list[tuple[pygame.Rect, str, str]] = []
        self.page = "home"
        self.notice = "Welcome home! Take good care of your friends."
        # World-space position and destination for the selected companion.
        self.pet_x = 510.0
        self.pet_y = 468.0
        self.target_x = self.pet_x
        self.target_y = self.pet_y
        self.next_wander = time.monotonic() + 2.0
        self.facing_left = False

    @property
    def pet(self) -> Pet:
        return next(
            (pet for pet in self.pets if pet.pet_id == self.selected_pet),
            self.pets[0],
        )

    def save(self) -> None:
        save_family(self.pets, self.pet.pet_id)
        save_economy(
            self.economy.get("coins", 120),
            self.economy.get("gems", 2),
            self.economy.get("gem_milestones", []),
        )
        self.last_save = time.monotonic()

    def label(self, text: str, x: int, y: int, color=TEXT, font=None) -> None:
        surface = (font or self.font).render(str(text), True, color)
        self.screen.blit(surface, (x, y))

    def panel(self, rect: pygame.Rect, color=PANEL, radius=14) -> None:
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

    def button(
        self, rect: pygame.Rect, text: str, key: str, *,
        active: bool = False, disabled: bool = False,
    ) -> None:
        color = ACCENT if active else PANEL_LIGHT
        if disabled:
            color = (47, 57, 69)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        ink = (18, 34, 39) if active else (MUTED if disabled else TEXT)
        rendered = self.font.render(text, True, ink)
        self.screen.blit(rendered, rendered.get_rect(center=rect.center))
        self.buttons.append((rect, key, text))

    def draw_background(self) -> None:
        self.screen.fill(BG)
        self.panel(pygame.Rect(14, 14, 204, 692))
        self.panel(pygame.Rect(230, 14, 560, 692))
        self.panel(pygame.Rect(802, 14, 284, 692))

    def draw_sidebar(self) -> None:
        self.label("🐾 CODEPAWS", 32, 31, ACCENT, self.heading)
        self.label("DESKTOP GAME", 33, 63, MUTED, self.small)
        self.button(pygame.Rect(25, 76, 182, 28), "+ Adopt a friend", "adoption")
        self.label("YOUR FAMILY", 32, 111, MUTED, self.small)
        for index, pet in enumerate(self.pets):
            y = 143 + index * 51
            if y > 635:
                break
            selected = pet.pet_id == self.pet.pet_id
            rect = pygame.Rect(25, y, 182, 43)
            pygame.draw.rect(
                self.screen,
                (54, 83, 91) if selected else PANEL_LIGHT,
                rect,
                border_radius=9,
            )
            self.label(pet.emoji, 35, y + 8, TEXT, self.heading)
            self.label(pet.name, 75, y + 5, TEXT)
            self.label(pet.technology, 75, y + 23, MUTED, self.small)
            self.buttons.append((rect, f"pet:{pet.pet_id}", pet.name))
        self.label(f"{len(self.pets)} companion(s)", 32, 658, MUTED, self.small)

    def draw_room(self) -> None:
        self.label("Your little home", 253, 29, TEXT, self.title)
        self.label("A cozy place for your programming family", 255, 65, MUTED, self.small)
        self.label(self.notice[:62], 255, 82, ACCENT, self.small)

        for index, (room_id, room_name) in enumerate(ROOMS):
            rect = pygame.Rect(250 + index * 171, 101, 158, 37)
            self.button(rect, room_name, f"room:{room_id}", active=self.pet.room == room_id)

        world = pygame.Rect(250, 153, 520, 382)
        room = self.pet.room
        if room == "bedroom":
            wall, floor = (67, 65, 105), (104, 83, 92)
        elif room == "garden":
            wall, floor = (89, 151, 133), (72, 119, 86)
        else:
            wall, floor = (91, 126, 145), (127, 100, 83)
        pygame.draw.rect(self.screen, wall, world, border_radius=13)
        pygame.draw.rect(self.screen, floor, (world.x, 435, world.width, 100),
                         border_radius=13)
        pygame.draw.rect(self.screen, (0, 0, 0), world, width=3, border_radius=13)

        # Simple room details give each space a recognizable silhouette.
        if room == "living":
            pygame.draw.rect(self.screen, (54, 76, 103), (290, 335, 155, 75),
                             border_radius=16)
            pygame.draw.rect(self.screen, (79, 106, 136), (280, 325, 175, 35),
                             border_radius=12)
            pygame.draw.rect(self.screen, (224, 190, 133), (605, 350, 95, 85),
                             border_radius=9)
            pygame.draw.rect(self.screen, (245, 216, 160), (615, 360, 75, 10),
                             border_radius=4)
            pygame.draw.rect(self.screen, (72, 94, 115), (480, 180, 100, 68),
                             border_radius=7)
            pygame.draw.rect(self.screen, (158, 213, 207), (488, 188, 84, 52),
                             border_radius=4)
            pygame.draw.circle(self.screen, (244, 205, 111), (530, 214), 13)
        elif room == "bedroom":
            pygame.draw.rect(self.screen, (64, 48, 78), (290, 345, 205, 78),
                             border_radius=12)
            pygame.draw.rect(self.screen, (205, 192, 218), (305, 330, 75, 38),
                             border_radius=10)
            pygame.draw.rect(self.screen, (126, 105, 151), (380, 330, 100, 92),
                             border_radius=10)
            pygame.draw.circle(self.screen, (250, 222, 153), (685, 205), 27)
            for x in (290, 700):
                pygame.draw.circle(self.screen, (247, 224, 161), (x, 180), 3)
        else:
            pygame.draw.circle(self.screen, (248, 217, 132), (680, 205), 34)
            for x, y in ((310, 390), (690, 385), (370, 475), (650, 475)):
                pygame.draw.rect(self.screen, (63, 96, 67), (x, y, 18, 48),
                                 border_radius=5)
                pygame.draw.circle(self.screen, (89, 157, 105), (x + 8, y - 5), 25)
                pygame.draw.circle(self.screen, (118, 184, 120), (x - 5, y + 8), 14)
            for x, y in ((430, 180), (590, 260), (350, 260), (620, 450)):
                pygame.draw.circle(self.screen, (255, 224, 139), (x, y), 4)

        # Companion wanders freely around the room's walkable floor.
        pygame.draw.ellipse(
            self.screen, (48, 57, 62),
            (int(self.pet_x - 43), int(self.pet_y - 9), 86, 19),
        )
        action = self.active_action if time.monotonic() < self.action_until else None
        sprite = _draw(self.pet, self.frame, action)
        pet_surface = pygame.image.fromstring(sprite.tobytes(), sprite.size, "RGB")
        pet_surface = pygame.transform.scale(pet_surface, (144, 144))
        if self.facing_left:
            pet_surface = pygame.transform.flip(pet_surface, True, False)
        self.screen.blit(pet_surface, (int(self.pet_x - 72), int(self.pet_y - 139)))
        self.label(self.pet.name, int(self.pet_x - 35), int(self.pet_y + 2), TEXT, self.heading)
        self.label(self.pet.mood, int(self.pet_x - 25), int(self.pet_y + 31), MUTED, self.small)

        actions = [
            ("Feed", "feed", (250, 590)),
            ("Play", "play", (381, 590)),
            ("Sleep", "sleep", (512, 590)),
            ("Bathe", "bathe", (643, 590)),
        ]
        for caption, key, (x, y) in actions:
            self.button(pygame.Rect(x, y, 119, 48), caption, f"action:{key}")

    def draw_adoption(self) -> None:
        """Show the mascot adoption center as an in-game screen."""
        from .models import PET_CATALOG

        self.label("Adoption Center", 265, 35, TEXT, self.title)
        self.label("Welcome another programming mascot to your family", 267, 75, MUTED, self.small)
        self.label(self.notice, 267, 108, ACCENT, self.small)
        adopted = {pet.pet_id for pet in self.pets}
        for index, entry in enumerate(PET_CATALOG):
            y = 145 + index * 51
            if y > 655:
                break
            rect = pygame.Rect(260, y, 500, 43)
            pygame.draw.rect(self.screen, PANEL_LIGHT, rect, border_radius=9)
            self.label(entry.get("emoji", "🐾"), 273, y + 7, TEXT, self.heading)
            self.label(entry["name"], 320, y + 5, TEXT)
            self.label(entry["technology"], 320, y + 24, MUTED, self.small)
            if entry["pet_id"] in adopted:
                caption, key, disabled = "Adopted", "noop", True
            else:
                price = 80 if index < 7 else 140
                caption, key, disabled = f"Adopt · {price} coins", f"adopt:{entry['pet_id']}", self.economy.get("coins", 0) < price
            self.button(pygame.Rect(610, y + 5, 138, 33), caption, key, disabled=disabled)

    def draw_stat(self, name: str, value: int, x: int, y: int, color) -> None:
        self.label(name, x, y, MUTED, self.small)
        self.label(f"{value}%", x + 218, y, TEXT, self.small)
        bar = pygame.Rect(x, y + 23, 242, 11)
        pygame.draw.rect(self.screen, (53, 67, 82), bar, border_radius=6)
        fill = bar.copy()
        fill.width = int(bar.width * max(0, min(100, value)) / 100)
        if fill.width:
            pygame.draw.rect(self.screen, color, fill, border_radius=6)

    def draw_stats(self) -> None:
        self.label("Companion", 824, 31, TEXT, self.title)
        self.label(f"{self.pet.name}  ·  {self.pet.technology}", 825, 70,
                   MUTED, self.small)
        self.panel(pygame.Rect(822, 106, 244, 82), PANEL_LIGHT, 12)
        self.label(f"LEVEL  {self.pet.level}", 840, 122, ACCENT, self.heading)
        self.label(f"{self.pet.experience} / {self.pet.experience_to_next_level} XP",
                   840, 156, TEXT, self.small)
        self.draw_stat("Happiness", self.pet.happiness, 824, 218, (242, 190, 102))
        self.draw_stat("Energy", self.pet.energy, 824, 286, (119, 190, 246))
        self.draw_stat("Hunger", 100 - self.pet.hunger, 824, 354, (237, 151, 113))
        self.draw_stat("Cleanliness", self.pet.cleanliness, 824, 422, (123, 211, 184))
        self.panel(pygame.Rect(822, 510, 244, 78), PANEL_LIGHT, 12)
        self.label("WALLET", 840, 523, MUTED, self.small)
        self.label(f"● {self.economy.get('coins', 0)} coins", 840, 548, TEXT)
        self.label(f"◆ {self.economy.get('gems', 0)} gems", 953, 548, TEXT)
        self.label("F / P / S / B  care shortcuts", 824, 623, MUTED, self.small)
        self.label("← →  switch companion", 824, 646, MUTED, self.small)
        self.label("1 / 2 / 3  change room", 824, 669, MUTED, self.small)

    def update_pet_motion(self, dt: float, now: float) -> None:
        """Move the companion smoothly and choose a new idle destination."""
        if self.page != "home":
            return
        if now >= self.next_wander and abs(self.pet_x - self.target_x) < 5:
            self.target_x = random.uniform(320, 710)
            self.target_y = random.uniform(452, 493)
            self.next_wander = now + random.uniform(2.0, 4.5)

        dx = self.target_x - self.pet_x
        dy = self.target_y - self.pet_y
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 1:
            speed = min(distance, 78 * dt)
            self.pet_x += dx / distance * speed
            self.pet_y += dy / distance * speed
            self.facing_left = dx < 0

    def move_pet_to(self, x: float, y: float) -> None:
        """Send the selected pet to a point on the room floor."""
        self.target_x = max(320.0, min(710.0, x))
        self.target_y = max(452.0, min(493.0, y))
        self.next_wander = time.monotonic() + 3.0

    def act(self, action: str) -> None:
        messages = {
            "feed": self.pet.feed,
            "play": self.pet.play,
            "sleep": self.pet.sleep,
            "bathe": self.pet.bathe,
        }
        if action in messages:
            result = messages[action]()
            if action == "play" and "too tired" in result:
                self.active_action = None
                return
            self.pet.gain_experience(8)
            self.active_action = action
            self.action_until = time.monotonic() + 2.0
            self.save()

    def switch_pet(self, step: int) -> None:
        current = next((i for i, pet in enumerate(self.pets)
                        if pet.pet_id == self.pet.pet_id), 0)
        self.selected_pet = self.pets[(current + step) % len(self.pets)].pet_id
        self.save()

    def handle_click(self, position: tuple[int, int]) -> None:
        for rect, key, _caption in reversed(self.buttons):
            if rect.collidepoint(position):
                if key.startswith("pet:"):
                    self.selected_pet = key.split(":", 1)[1]
                    self.save()
                elif key.startswith("room:"):
                    self.pet.room = key.split(":", 1)[1]
                    self.save()
                elif key == "adoption":
                    self.page = "adoption"
                elif key.startswith("adopt:"):
                    pet_id = key.split(":", 1)[1]
                    from .models import PET_CATALOG
                    entry = next((item for item in PET_CATALOG if item["pet_id"] == pet_id), None)
                    if entry and pet_id not in {pet.pet_id for pet in self.pets}:
                        index = PET_CATALOG.index(entry)
                        price = 80 if index < 7 else 140
                        if self.economy.get("coins", 0) >= price:
                            self.economy["coins"] -= price
                            self.pets.append(create_pet(pet_id))
                            self.selected_pet = pet_id
                            self.notice = f"Welcome to the family, {entry['name']}!"
                            self.save()
                        else:
                            self.notice = "You need more coins to adopt this friend."
                elif key.startswith("action:"):
                    self.act(key.split(":", 1)[1])
                return

        # Clicking the room floor gives the companion a destination.
        x, y = position
        if self.page == "home" and 250 <= x <= 770 and 435 <= y <= 535:
            self.move_pet_to(x, y)
            self.notice = f"{self.pet.name} is exploring the room."
        # Clicking room objects sends the pet over for a little visit.
        elif self.page == "home" and 250 <= x <= 770 and 153 <= y <= 435:
            room = self.pet.room
            if room == "living" and 275 <= x <= 460 and 315 <= y <= 420:
                self.move_pet_to(380, 466)
                self.notice = f"{self.pet.name} is visiting the sofa."
            elif room == "bedroom" and 280 <= x <= 500 and 320 <= y <= 430:
                self.move_pet_to(420, 466)
                self.notice = f"{self.pet.name} is visiting the bed."
            elif room == "garden" and (x < 390 or x > 650):
                self.move_pet_to(520, 466)
                self.notice = f"{self.pet.name} is exploring the garden."

    def handle_key(self, key: int) -> None:
        shortcuts = {
            pygame.K_f: "feed", pygame.K_p: "play",
            pygame.K_s: "sleep", pygame.K_b: "bathe",
        }
        if key in shortcuts:
            self.act(shortcuts[key])
        elif key == pygame.K_LEFT:
            self.switch_pet(-1)
        elif key == pygame.K_RIGHT:
            self.switch_pet(1)
        elif key == pygame.K_a:
            self.page = "adoption"
        elif key == pygame.K_ESCAPE and self.page == "adoption":
            self.page = "home"
        elif key in (pygame.K_1, pygame.K_2, pygame.K_3):
            self.pet.room = ROOMS[key - pygame.K_1][0]
            self.save()

    def run(self) -> None:
        while self.running:
            now = time.monotonic()
            dt = min(self.clock.get_time() / 1000.0, 0.05)
            self.frame = int(now * 7) % 10000
            self.update_pet_motion(dt, now)
            if now - self.last_tick >= 30:
                for companion in self.pets:
                    companion.pass_time()
                self.last_tick = now
            if now - self.last_save >= 90:
                self.save()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.page == "home":
                        self.running = False
                    else:
                        self.handle_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.buttons = []
            self.draw_background()
            self.draw_sidebar()
            if self.page == "adoption":
                self.draw_adoption()
            else:
                self.draw_room()
                self.draw_stats()
            pygame.display.flip()
            self.clock.tick(30)

        self.save()
        pygame.quit()


def run() -> None:
    """Launch the CodePaws desktop game."""
    try:
        CodePawsDesktop().run()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    run()
