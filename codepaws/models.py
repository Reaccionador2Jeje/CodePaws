"""Pet models and the adoption catalog."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Pet:
    pet_id: str
    name: str
    technology: str
    species: str
    personality: str
    art: str
    happiness: int = 80
    energy: int = 75
    hunger: int = 20
    cleanliness: int = 90
    emoji: str = "🐾"
    color: str = "#7ee0b5"
    level: int = 1
    experience: int = 0

    @property
    def experience_to_next_level(self) -> int:
        return max(100, self.level * 100)

    def gain_experience(self, amount: int) -> int:
        """Add experience and return the number of levels gained."""
        self.experience += max(0, amount)
        levels_gained = 0
        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level += 1
            levels_gained += 1
        return levels_gained

    def clamp(self) -> None:
        for field in ("happiness", "energy", "hunger", "cleanliness"):
            setattr(self, field, max(0, min(100, getattr(self, field))))

    @property
    def mood(self) -> str:
        if self.hunger >= 80:
            return "Hungry"
        if self.energy <= 20:
            return "Sleepy"
        if self.cleanliness <= 20:
            return "Needs a bath"
        if self.happiness >= 80:
            return "Very happy"
        if self.happiness <= 30:
            return "A little sad"
        return "Happy"

    def feed(self) -> str:
        self.hunger -= 25
        self.happiness += 4
        self.clamp()
        return f"{self.name} enjoyed the snack!"

    def play(self) -> str:
        if self.energy < 15:
            return f"{self.name} is too tired to play right now."
        self.happiness += 18
        self.energy -= 15
        self.hunger += 10
        self.clamp()
        return f"{self.name} had a lovely playtime!"

    def sleep(self) -> str:
        self.energy += 35
        self.hunger += 5
        self.clamp()
        return f"{self.name} had a refreshing nap."

    def bathe(self) -> str:
        self.cleanliness = 100
        self.happiness += 5
        self.clamp()
        return f"{self.name} is all clean!"

    def pass_time(self) -> None:
        self.hunger += 2
        self.energy -= 1
        self.cleanliness -= 1
        self.happiness -= 1
        self.clamp()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pet":
        # Older save files do not contain progression fields.
        return cls(**data)


PET_CATALOG: list[dict[str, str]] = [
    {
        "pet_id": "python",
        "name": "Py",
        "technology": "Python",
        "species": "Programming snake",
        "personality": "Curious, friendly and a little sleepy.",
        "emoji": "🐍",
        "color": "#4caf50",
        "art": r"""
  /^\/^\\
 _|  o.o  |_
   \  ^  /
    |||||
""".strip("\n"),
    },
    {
        "pet_id": "rust",
        "name": "Ferris",
        "technology": "Rust",
        "species": "Rustacean crab",
        "personality": "Brave, energetic and protective.",
        "emoji": "🦀",
        "color": "#f05a47",
        "art": r"""
  .-'''-.
 /  o o  \
|    ^    |
 \  ---  /
  '-----'
""".strip("\n"),
    },
    {
        "pet_id": "go",
        "name": "Gopher",
        "technology": "Go",
        "species": "Gopher",
        "personality": "Quick, helpful and hardworking.",
        "emoji": "🐹",
        "color": "#48a9e6",
        "art": r"""
  .-'''-.
 /  o o  \
|    w    |
|  _____  |
 '-------'
""".strip("\n"),
    },
    {
        "pet_id": "java",
        "name": "Duke",
        "technology": "Java",
        "species": "Java mascot",
        "personality": "Calm, dependable and elegant.",
        "emoji": "☕",
        "color": "#e07b39",
        "art": r"""
   .---.
  /     \
 |  o o  |
 |   ^   |
  \_____/
""".strip("\n"),
    },
    {
        "pet_id": "docker",
        "name": "Moby",
        "technology": "Docker",
        "species": "Container whale",
        "personality": "Gentle, big-hearted and always carrying friends.",
        "emoji": "🐳",
        "color": "#249bd3",
        "art": r"""
      __
 ___ /  \___
/  _| [] []  \
\____________/
""".strip("\n"),
    },
    {
        "pet_id": "github",
        "name": "Octocat",
        "technology": "GitHub",
        "species": "Octocat",
        "personality": "Creative, social and adventurous.",
        "emoji": "🐙",
        "color": "#9b6bd3",
        "art": r"""
 /\\_/\\
( o   o )
 /  ^  \
/|     |\\
 \_____/
""".strip("\n"),
    },
    {
        "pet_id": "gitlab",
        "name": "Tanuki",
        "technology": "GitLab",
        "species": "Tanuki",
        "personality": "Organized, clever and collaborative.",
        "emoji": "🦝",
        "color": "#f28c45",
        "art": r"""
 /\   /\\
(  o o  )
(   ^   )
 /|___|\\
  /   \
""".strip("\n"),
    },
    {
        "pet_id": "php",
        "name": "ElePHPant",
        "technology": "PHP",
        "species": "Blue elephant",
        "personality": "Friendly, patient and great at carrying web projects.",
        "art": "🐘",
        "emoji": "🐘",
        "color": "#8899ff",
    },
    {
        "pet_id": "javascript",
        "name": "Javie",
        "technology": "JavaScript",
        "species": "Yellow script sprite",
        "personality": "Playful, energetic and always experimenting.",
        "art": "🟨",
        "emoji": "🟨",
        "color": "#f7df1e",
    },
    {
        "pet_id": "typescript",
        "name": "Tessa",
        "technology": "TypeScript",
        "species": "Blue crystal sprite",
        "personality": "Careful, clever and loves clear structure.",
        "art": "💠",
        "emoji": "💠",
        "color": "#3178c6",
    },
    {
        "pet_id": "ruby",
        "name": "Ruby",
        "technology": "Ruby",
        "species": "Gem creature",
        "personality": "Creative, warm and loves elegant solutions.",
        "art": "💎",
        "emoji": "💎",
        "color": "#e45b75",
    },
    {
        "pet_id": "c",
        "name": "Cee",
        "technology": "C",
        "species": "Tiny robot",
        "personality": "Simple, fast and close to the machine.",
        "art": "🤖",
        "emoji": "🤖",
        "color": "#a8b3c2",
    },
    {
        "pet_id": "cpp",
        "name": "PlusPlus",
        "technology": "C++",
        "species": "Gear robot",
        "personality": "Powerful, inventive and loves building things.",
        "art": "⚙️",
        "emoji": "⚙️",
        "color": "#659ad2",
    },
    {
        "pet_id": "kotlin",
        "name": "Koko",
        "technology": "Kotlin",
        "species": "Purple cat",
        "personality": "Expressive, modern and loves mobile adventures.",
        "art": "🐈",
        "emoji": "🐈",
        "color": "#a97bff",
    },
    {
        "pet_id": "swift",
        "name": "Swiftie",
        "technology": "Swift",
        "species": "Swift bird",
        "personality": "Quick, bright and loves smooth experiences.",
        "art": "🐦",
        "emoji": "🐦",
        "color": "#f28c45",
    },
    {
        "pet_id": "perl",
        "name": "Camel",
        "technology": "Perl",
        "species": "Desert camel",
        "personality": "Resourceful, adaptable and full of surprises.",
        "art": "🐪",
        "emoji": "🐪",
        "color": "#54a6a6",
    },
]


def create_pet(pet_id: str) -> Pet:
    """Create a fresh pet from the adoption catalog."""
    entry = next((item for item in PET_CATALOG if item["pet_id"] == pet_id), None)
    if entry is None:
        raise ValueError(f"Unknown pet: {pet_id}")
    return Pet(**entry)
