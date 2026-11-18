"""Full-screen Textual interface for CodePaws."""

from __future__ import annotations

import time

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from .models import PET_CATALOG, Pet, create_pet
from .storage import load_family, save_family


class CodePawsApp(App[None]):
    TITLE = "CodePaws"
    SUB_TITLE = "Your Programming Family"

    CSS = """
    Screen {
        background: #101820;
        color: #e8f1f2;
    }
    #main-layout {
        height: 1fr;
    }
    #sidebar {
        width: 25;
        min-width: 22;
        padding: 1 1;
        background: #172630;
        border-right: solid #31515b;
    }
    #brand {
        height: 3;
        content-align: center middle;
        color: #7ee0b5;
        text-style: bold;
    }
    #tagline {
        height: 2;
        content-align: center middle;
        color: #91a8b2;
    }
    #nav-title {
        margin-top: 1;
        color: #7ee0b5;
        text-style: bold;
    }
    #sidebar Button {
        width: 100%;
        margin: 0 0 1 0;
    }
    #sidebar-note {
        dock: bottom;
        height: 4;
        color: #91a8b2;
        content-align: center middle;
    }
    #content {
        width: 1fr;
        padding: 1 2;
    }
    .page-title {
        color: #7ee0b5;
        text-style: bold;
        margin-bottom: 1;
    }
    .muted {
        color: #91a8b2;
    }
    #pet-stage {
        background: #172630;
        color: #e8f1f2;
        content-align: center middle;
        height: auto;
        min-height: 13;
        width: 1fr;
        border: round #42616d;
        margin: 1 0;
        padding: 2 3;
    }
    .pet-subtitle {
        color: #91a8b2;
        margin-bottom: 1;
    }
    .stat {
        margin: 0 0 1 0;
        color: #d7e5e8;
    }
    .stat {
        margin: 0 0 1 0;
    }
    .action-row {
        height: auto;
        margin-top: 1;
    }
    .action-row Button {
        margin-right: 1;
    }
    .catalog-card {
        border: round #31515b;
        padding: 1;
        margin: 0 0 1 0;
        height: auto;
    }
    .catalog-card Button {
        margin-top: 1;
    }
    .notice {
        color: #f4d58d;
        margin: 1 0;
    }
    .wallet {
        background: #203440;
        border: round #42616d;
        color: #f4d58d;
        padding: 1 2;
        margin: 1 0;
        text-style: bold;
    }
    """

    BINDINGS = [
        ("h", "show_page('home')", "Home"),
        ("a", "show_page('adoption')", "Adopt"),
        ("f", "show_page('family')", "Family"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.pets, self.selected_pet_id = load_family()
        self.coins = 120
        self.gems = 2
        self.gem_milestones: set[int] = set()
        self.last_coin_reward = 0.0
        self.load_economy()
        self.page = "home"
        self.notice = "Welcome home! Your programming family starts here."
        self.active_action: str | None = None
        self.action_ticks = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-layout"):
            with Vertical(id="sidebar"):
                yield Static("🐾 CODEPAWS", id="brand")
                yield Static("A little home for code", id="tagline")
                yield Static("NAVIGATION", id="nav-title")
                yield Button("⌂  Home", id="nav-home", variant="primary")
                yield Button("+  Adoption Center", id="nav-adoption")
                yield Button("♥  My Family", id="nav-family")
                yield Button("✦  About", id="nav-about")
                yield Static(
                    "Take care. Play often.\nAdopt them all!",
                    id="sidebar-note",
                )
            yield VerticalScroll(id="content")
        yield Footer()

    async def on_mount(self) -> None:
        self.set_interval(60, self.pass_time)
        self.set_interval(0.8, self.animate_pet)
        await self.refresh_view()

    def action_show_page(self, page: str) -> None:
        self.page = page
        self.run_worker(self.refresh_view(), exclusive=True)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id or ""

        if button_id == "welcome-adoption":
            self.page = "adoption"
            await self.refresh_view()
            return

        if button_id.startswith("nav-"):
            self.page = button_id.removeprefix("nav-")
            await self.refresh_view()
            return

        if button_id.startswith("adopt-"):
            pet_id = button_id.removeprefix("adopt-")
            entry = next((item for item in PET_CATALOG if item["pet_id"] == pet_id), None)
            if pet_id in {pet.pet_id for pet in self.pets}:
                self.notice = "That friend has already been adopted!"
            elif entry is None:
                self.notice = "That mascot is not available."
            else:
                coin_cost, gem_cost = self.adoption_price(entry)
                if self.coins < coin_cost or self.gems < gem_cost:
                    self.notice = f"Not enough currency! Need {coin_cost} coins" + (f" and {gem_cost} gems." if gem_cost else ".")
                else:
                    self.coins -= coin_cost
                    self.gems -= gem_cost
                    pet = create_pet(pet_id)
                    self.pets.append(pet)
                    self.selected_pet_id = pet.pet_id
                    self.notice = f"{pet.name} joined your family! (-{coin_cost} coins, -{gem_cost} gems)"
                    self.page = "family"
                    self.check_gem_milestones()
            self.persist()
            await self.refresh_view()
            return

        if button_id.startswith("select-"):
            self.selected_pet_id = button_id.removeprefix("select-")
            self.persist()
            self.page = "home"
            await self.refresh_view()
            return

        if button_id.startswith("pet-"):
            self.handle_pet_action(button_id.removeprefix("pet-"))
            self.persist()
            await self.refresh_view()

    def handle_pet_action(self, action: str) -> None:
        pet = self.selected_pet
        if pet is None:
            self.notice = "Adopt a pet first!"
            return

        actions = {
            "feed": pet.feed,
            "play": pet.play,
            "sleep": pet.sleep,
            "bath": pet.bathe,
        }
        callback = actions.get(action)
        if callback is not None:
            before = (pet.happiness, pet.energy, pet.hunger, pet.cleanliness)
            self.notice = callback()
            after = (pet.happiness, pet.energy, pet.hunger, pet.cleanliness)
            if before != after and time.monotonic() - self.last_coin_reward >= 10:
                earned = {"feed": 5, "play": 8, "sleep": 3, "bath": 4}[action]
                self.coins += earned
                self.last_coin_reward = time.monotonic()
                self.notice += f"  (+{earned} coins)"
            elif before != after:
                self.notice += "  (Coin reward cooldown: wait a few seconds.)"
            self.active_action = action
            self.action_ticks = 10

    def adoption_price(self, entry: dict) -> tuple[int, int]:
        index = next(i for i, item in enumerate(PET_CATALOG) if item["pet_id"] == entry["pet_id"])
        if index < 7:
            return 80, 0
        if index < 12:
            return 140, 0
        return 180, 1

    def load_economy(self) -> None:
        from .storage import load_economy
        data = load_economy()
        self.coins = max(0, int(data.get("coins", self.coins)))
        self.gems = max(0, int(data.get("gems", self.gems)))
        self.gem_milestones = set(data.get("gem_milestones", []))

    def check_gem_milestones(self) -> None:
        for milestone, reward in ((3, 2), (6, 3), (10, 5)):
            if len(self.pets) >= milestone and milestone not in self.gem_milestones:
                self.gems += reward
                self.gem_milestones.add(milestone)
                self.notice += f"  💎 Milestone: +{reward} gems!"

    @property
    def selected_pet(self) -> Pet | None:
        return next(
            (pet for pet in self.pets if pet.pet_id == self.selected_pet_id),
            self.pets[0] if self.pets else None,
        )

    def persist(self) -> None:
        save_family(self.pets, self.selected_pet_id)
        from .storage import save_economy
        save_economy(self.coins, self.gems, sorted(self.gem_milestones))

    def animate_pet(self) -> None:
        """Refresh the modern mascot card and briefly show care reactions."""
        pet = self.selected_pet
        if pet is None or self.page != "home":
            return
        if self.action_ticks > 0:
            self.action_ticks -= 1
            if self.action_ticks == 0:
                self.active_action = None
        try:
            self.query_one("#pet-stage", Static).update(self.pet_visual(pet))
        except Exception:
            # The home screen may be transitioning between pages.
            pass

    def pass_time(self) -> None:
        if not self.pets:
            return
        for pet in self.pets:
            pet.pass_time()
        self.persist()
        self.run_worker(self.refresh_view(), exclusive=True)

    async def refresh_view(self) -> None:
        content = self.query_one("#content", VerticalScroll)
        await content.remove_children()
        widgets = self.build_page()
        await content.mount(*widgets)

    def build_page(self) -> list:
        if self.page == "adoption":
            return self.build_adoption_page()
        if self.page == "family":
            return self.build_family_page()
        if self.page == "about":
            return self.build_about_page()
        return self.build_home_page()

    def build_home_page(self) -> list:
        pet = self.selected_pet
        if pet is None:
            return [
                Static("WELCOME TO CODEPAWS", classes="page-title"),
                Static(self.wallet_line(), classes="wallet"),
                Static(
                    "Your home is ready, but nobody lives here yet.\n"
                    "Visit the Adoption Center to welcome your first friend!",
                ),
                Static(self.notice, classes="notice"),
                Button("Open Adoption Center", id="welcome-adoption", variant="success"),
            ]

        return [
            Static("YOUR LITTLE HOME", classes="page-title"),
            Static(self.wallet_line(), classes="wallet"),
            Static(self.notice, classes="notice"),
            Static(f"Meet {pet.name}  ·  {pet.technology}", classes="page-title"),
            Static(
                self.pet_visual(pet),
                id="pet-stage",
                markup=True,
            ),
            Static(f"{pet.species}  ·  {pet.mood}", classes="pet-subtitle"),
            Static(pet.personality, classes="muted"),
            Static(self.stat_line("Happiness", pet.happiness), classes="stat"),
            Static(self.stat_line("Energy", pet.energy), classes="stat"),
            Static(self.stat_line("Fullness", 100 - pet.hunger), classes="stat"),
            Static(self.stat_line("Cleanliness", pet.cleanliness), classes="stat"),
            Static("CARE ACTIONS", classes="page-title"),
            Horizontal(
                Button("Feed", id="pet-feed", variant="success"),
                Button("Play", id="pet-play", variant="primary"),
                Button("Sleep", id="pet-sleep"),
                Button("Bath", id="pet-bath"),
                classes="action-row",
            ),
            Static(
                f"Family members: {len(self.pets)}    "
                "Adopt more friends from the Adoption Center.",
                classes="muted",
            ),
        ]

    def wallet_line(self) -> str:
        return f"[bold #f4d58d]◉ {self.coins} coins[/]    [bold #8bd5ff]◆ {self.gems} gems[/]"

    def pet_visual(self, pet: Pet) -> str:
        """Build a colorful, responsive mascot card with Rich markup."""
        action_messages = {
            "feed": "🍪  SNACK TIME!  •  YUM YUM!",
            "play": "🎉  PLAY MODE!  •  WHEEEE!",
            "sleep": "💤  NAP TIME  •  Zzz...",
            "bath": "🫧  SPLASH!  •  FRESH & CLEAN",
        }
        reaction = action_messages.get(self.active_action, "✨  HAPPY TO BE HERE  ✨")
        color = pet.color
        return (
            f"[bold {color}]{pet.emoji}[/]\n"
            f"[bold white]{pet.name}[/]\n"
            f"[bold {color}]{pet.technology.upper()}[/]\n"
            f"[dim]{pet.species}[/]\n"
            f"[bold white]{reaction}[/]"
        )

    @staticmethod
    def stat_line(label: str, value: int) -> str:
        filled = round(value / 10)
        bar = "█" * filled + "░" * (10 - filled)
        color = "#7ee0b5" if value >= 60 else "#f4d58d" if value >= 30 else "#ff7b86"
        return f"[bold]{label:<13}[/] [{color}]{bar}[/] {value:>3}%"

    def build_adoption_page(self) -> list:
        adopted = {pet.pet_id for pet in self.pets}
        widgets = [
            Static("ADOPTION CENTER", classes="page-title"),
            Static(
                "Every language and tool deserves a loving home. "
                "Choose your next family member!",
                classes="muted",
            ),
            Static(self.wallet_line(), classes="wallet"),
            Static(self.notice, classes="notice"),
        ]
        for entry in PET_CATALOG:
            already_adopted = entry["pet_id"] in adopted
            coin_cost, gem_cost = self.adoption_price(entry)
            affordable = self.coins >= coin_cost and self.gems >= gem_cost
            price = f"◉ {coin_cost} coins" + (f"  ◆ {gem_cost} gems" if gem_cost else "")
            widgets.append(
                Static(
                    f"{entry.get('emoji', '🐾')}  [bold {entry.get('color', '#7ee0b5')}]{entry['name']}[/]  ·  {entry['technology']}\n"
                    f"[dim]{entry['species']}[/]\n{entry['personality']}\n"
                    f"[bold #f4d58d]{price}[/]",
                    classes="catalog-card",
                )
            )
            widgets.append(
                Button(
                    "Already adopted" if already_adopted else ("Adopt " + entry["name"] if affordable else "Not enough currency"),
                    id=f"adopt-{entry['pet_id']}",
                    disabled=already_adopted or not affordable,
                    variant="success" if affordable and not already_adopted else "default",
                )
            )
        return widgets

    def build_family_page(self) -> list:
        widgets = [
            Static("YOUR PROGRAMMING FAMILY", classes="page-title"),
            Static(self.notice, classes="notice"),
        ]
        if not self.pets:
            widgets.append(Static("Your family album is empty. Adopt your first pet!"))
            widgets.append(Button("Visit Adoption Center", id="welcome-adoption"))
            return widgets

        for pet in self.pets:
            selected = pet.pet_id == self.selected_pet_id
            widgets.append(
                Static(
                    f"{'★ ' if selected else ''}{pet.emoji}  [bold {pet.color}]{pet.name}[/] — {pet.technology} "
                    f"| {pet.mood} | Happiness {pet.happiness}%",
                    classes="catalog-card",
                )
            )
            widgets.append(
                Button(
                    "Currently selected" if selected else f"Spend time with {pet.name}",
                    id=f"select-{pet.pet_id}",
                    disabled=selected,
                )
            )
        widgets.append(Static(f"Together: {len(self.pets)} happy family member(s)!"))
        return widgets

    def build_about_page(self) -> list:
        return [
            Static("ABOUT CODEPAWS", classes="page-title"),
            Static("CodePaws 0.4.0 — Your Programming Family"),
            Static(
                "A full-screen terminal pet simulator where programming "
                "languages, tools and platforms become digital companions."
            ),
            Static("Made with Python, Textual and a little love. ♥", classes="muted"),
            Static("Keyboard shortcuts: H = Home · A = Adopt · F = Family · Q = Quit"),
        ]


def run() -> None:
    CodePawsApp().run()
