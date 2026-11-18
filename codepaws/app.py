"""Full-screen Textual interface for CodePaws."""

from __future__ import annotations

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
        color: #7ee0b5;
        text-style: bold;
        content-align: center middle;
        height: auto;
        min-height: 18;
        width: 1fr;
        border: double #7ee0b5;
        margin: 1 0;
        padding: 1 2;
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
        self.page = "home"
        self.notice = "Welcome home! Your programming family starts here."
        self.animation_frame = 0
        self.animation_frames = {
            "python": [
                "          .--------.\n"
                "         /  o    o  /\n"
                "        |    ^     |\n"
                "        |          |\n"
                "         '--------'\n"
                "       /|          |",
                "          .--------.\n"
                "         /  -    -  /\n"
                "        |    w     |\n"
                "        |          |\n"
                "         '--------'\n"
                "       /|          |",
            ],
            "rust": [
                "        .----------.\n"
                "      .'  o      o  '.\n"
                "     /       ^        /\n"
                "    |    .------.     |\n"
                "     '._/________\__.'\n"
                "        / /    / /",
                "        .----------.\n"
                "      .'  ^      ^  '.\n"
                "     /       w        /\n"
                "    |    .------.     |\n"
                "     '._/________\__.'\n"
                "        / /    / /",
            ],
            "go": [
                "          .--------.\n"
                "        .'  o    o  '.\n"
                "       /      __      /\n"
                "      |    .-'  '-.   |\n"
                "      |   |  /  |  |  |\n"
                "       '._ '----' _.'\n"
                "          '------'",
                "          .--------.\n"
                "        .'  -    -  '.\n"
                "       /      ww      /\n"
                "      |    .-'  '-.   |\n"
                "      |   |  /  |  |  |\n"
                "       '._ '----' _.'\n"
                "          '------'",
            ],
            "java": [
                "          .==========.\n"
                "        .'   .----.   '.\n"
                "       /    / o  o /    /\n"
                "      |    |   ^  |     |\n"
                "      |    |      |     |\n"
                "       '._  '----'  _.'\n"
                "          '========'",
                "          .==========.\n"
                "        .'   .----.   '.\n"
                "       /    / -  - /    /\n"
                "      |    |   w  |     |\n"
                "      |    |      |     |\n"
                "       '._  '----'  _.'\n"
                "          '========'",
            ],
            "docker": [
                "             __________________\n"
                "       _____/  []  []  []       /\n"
                "   ___/   []  []  []  []       /\n"
                "  /   o                       /\n"
                "  |       .------------------'\n"
                "   '------'\n"
                "       ~ ~ ~ ~ ~ ~ ~ ~",
                "             __________________\n"
                "       _____/  []  []  []       /\n"
                "   ___/   []  []  []  []       /\n"
                "  /   ^                       /\n"
                "  |       .------------------'\n"
                "   '------'\n"
                "       ~ ~ ~ ~ ~ ~ ~ ~",
            ],
            "github": [
                "           /------/\n"
                "         .'  o  o  '.\n"
                "        /     __     /\n"
                "       |    .'  '.   |\n"
                "       |   /      /  |\n"
                "        '._      _.'\n"
                "          /|    |/\n"
                "         /_|____|_",
                "           /------/\n"
                "         .'  -  -  '.\n"
                "        /      w     /\n"
                "       |    .'  '.   |\n"
                "       |   /      /  |\n"
                "        '._      _.'\n"
                "          /|    |/\n"
                "         /_|____|_",
            ],
            "gitlab": [
                "          /----------/\n"
                "        .'   .----.   '.\n"
                "       /    / o  o /    /\n"
                "      |    |   ^  |     |\n"
                "      |     '----'      |\n"
                "       '._          _.'\n"
                "          /|      |/\n"
                "         /_|______|_",
                "          /----------/\n"
                "        .'   .----.   '.\n"
                "       /    / -  - /    /\n"
                "      |    |   w  |     |\n"
                "      |     '----'      |\n"
                "       '._          _.'\n"
                "          /|      |/\n"
                "         /_|______|_",
            ],
        }
        self.active_action: str | None = None
        self.action_frame = 0
        self.action_ticks = 0
        self.action_frames = {
            "feed": [
                "          (  .  .  )\n"
                "             \\__/\n"
                "          .-========-.\n"
                "         /   YUMMY!   \\\n"
                "         \\____________/\n"
                "              \\  🍪",
                "          (  ^  ^  )\n"
                "             \\__/\n"
                "          .-========-.\n"
                "         /  NOM NOM!  \\\n"
                "         \\____________/\n"
                "              \\  🍪",
            ],
            "play": [
                "       *       .       *\n"
                "          \\  ^_^  /\n"
                "       --- (  > <  ) ---\n"
                "          /   |   \\\n"
                "       *      |      *\n"
                "            _/ \\_",
                "    *    .    \\o/    .    *\n"
                "           ( ^o^ )\n"
                "       --- /|   |\\ ---\n"
                "          / |   | \\\n"
                "       *    /   \\    *",
            ],
            "sleep": [
                "          .-========-.\n"
                "         /  -     -   \\\n"
                "        |      z      |\n"
                "        |   Z         |\n"
                "         \\___________/\n"
                "             (___)",
                "          .-========-.\n"
                "         /  -     -   \\\n"
                "        |       Z     |\n"
                "        |   z          |\n"
                "         \\___________/\n"
                "            (____)",
            ],
            "bath": [
                "          .-========-.\n"
                "         /  o     o   \\\n"
                "        |    SPLASH!  |\n"
                "      ~~~\\___________/~~~\n"
                "          o   o   o\n"
                "            __|__",
                "       o  .-========-.  o\n"
                "         /  ^     ^   \\\n"
                "        |   SO FRESH! |\n"
                "      ~~~\\___________/~~~\n"
                "          o   o   o\n"
                "            __|__",
            ],
        }

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
        self.set_interval(0.65, self.animate_pet)
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
            if pet_id in {pet.pet_id for pet in self.pets}:
                self.notice = "That friend has already been adopted!"
            else:
                pet = create_pet(pet_id)
                self.pets.append(pet)
                self.selected_pet_id = pet.pet_id
                self.notice = f"{pet.name} joined your programming family!"
                self.page = "family"
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
            self.notice = callback()
            self.active_action = action
            self.action_frame = 0
            self.action_ticks = 12

    @property
    def selected_pet(self) -> Pet | None:
        return next(
            (pet for pet in self.pets if pet.pet_id == self.selected_pet_id),
            self.pets[0] if self.pets else None,
        )

    def persist(self) -> None:
        save_family(self.pets, self.selected_pet_id)

    def animate_pet(self) -> None:
        """Advance either a care animation or the mascot's idle animation."""
        pet = self.selected_pet
        if pet is None or self.page != "home":
            return

        if self.active_action and self.action_ticks > 0:
            frames = self.action_frames[self.active_action]
            art = frames[self.action_frame % len(frames)]
            self.action_frame += 1
            self.action_ticks -= 1
            if self.action_ticks == 0:
                self.active_action = None
        else:
            frames = self.animation_frames.get(pet.pet_id)
            if not frames:
                return
            self.animation_frame = (self.animation_frame + 1) % len(frames)
            art = frames[self.animation_frame]

        try:
            self.query_one("#pet-stage", Static).update(self.scale_ascii(art))
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
                Static(
                    "Your home is ready, but nobody lives here yet.\n"
                    "Visit the Adoption Center to welcome your first friend!",
                ),
                Static(self.notice, classes="notice"),
                Button("Open Adoption Center", id="welcome-adoption", variant="success"),
            ]

        return [
            Static("YOUR LITTLE HOME", classes="page-title"),
            Static(self.notice, classes="notice"),
            Static(f"Meet {pet.name}  ·  {pet.technology}", classes="page-title"),
            Static(
                self.current_pet_art(pet),
                id="pet-stage",
                markup=False,
                expand=True,
            ),
            Static(f"{pet.species}  |  Mood: {pet.mood}"),
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

    def current_pet_art(self, pet: Pet) -> str:
        if self.active_action and self.action_ticks > 0:
            frames = self.action_frames[self.active_action]
            return self.scale_ascii(frames[self.action_frame % len(frames)])

        frames = self.animation_frames.get(pet.pet_id)
        art = frames[self.animation_frame % len(frames)] if frames else pet.art
        return self.scale_ascii(art)

    @staticmethod
    def scale_ascii(art: str) -> str:
        """Make each mascot feel like a large centerpiece in the terminal."""
        enlarged_lines = []
        for line in art.splitlines():
            wide_line = "".join(character * 2 for character in line)
            enlarged_lines.extend((wide_line, wide_line))
        return "\n".join(enlarged_lines)

    @staticmethod
    def stat_line(label: str, value: int) -> str:
        filled = round(value / 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"{label:<13} [{bar}] {value:>3}%"

    def build_adoption_page(self) -> list:
        adopted = {pet.pet_id for pet in self.pets}
        widgets = [
            Static("ADOPTION CENTER", classes="page-title"),
            Static(
                "Every language and tool deserves a loving home. "
                "Choose your next family member!",
                classes="muted",
            ),
            Static(self.notice, classes="notice"),
        ]
        for entry in PET_CATALOG:
            already_adopted = entry["pet_id"] in adopted
            widgets.append(
                Static(
                    f"{entry['name']}  ·  {entry['technology']}\n"
                    f"{entry['species']}\n{entry['personality']}",
                    classes="catalog-card",
                )
            )
            widgets.append(
                Button(
                    "Already adopted" if already_adopted else f"Adopt {entry['name']}",
                    id=f"adopt-{entry['pet_id']}",
                    disabled=already_adopted,
                    variant="success" if not already_adopted else "default",
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
                    f"{'★ ' if selected else ''}{pet.name} — {pet.technology} "
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
            Static("CodePaws 0.2.0 — Your Programming Family"),
            Static(
                "A full-screen terminal pet simulator where programming "
                "languages, tools and platforms become digital companions."
            ),
            Static("Made with Python, Textual and a little love. ♥", classes="muted"),
            Static("Keyboard shortcuts: H = Home · A = Adopt · F = Family · Q = Quit"),
        ]


def run() -> None:
    CodePawsApp().run()
