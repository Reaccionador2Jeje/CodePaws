"""JSON save-file handling for CodePaws."""

import json
from pathlib import Path
from typing import Any

from .models import Pet

SAVE_PATH = Path("data/save.json")


def save_family(pets: list[Pet], selected_pet: str | None = None) -> None:
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "version": 1,
        "selected_pet": selected_pet,
        "pets": [pet.to_dict() for pet in pets],
    }
    temporary_path = SAVE_PATH.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_path.replace(SAVE_PATH)


def load_family() -> tuple[list[Pet], str | None]:
    if not SAVE_PATH.exists():
        return [], None

    try:
        payload = json.loads(SAVE_PATH.read_text(encoding="utf-8"))
        pets = [Pet.from_dict(item) for item in payload.get("pets", [])]
        selected = payload.get("selected_pet")
        if selected not in {pet.pet_id for pet in pets}:
            selected = pets[0].pet_id if pets else None
        return pets, selected
    except (OSError, ValueError, TypeError, KeyError):
        # Keep a damaged save file untouched so the player can recover it.
        return [], None


ECONOMY_PATH = Path("data/economy.json")


def save_economy(coins: int, gems: int, gem_milestones: list[int]) -> None:
    """Persist wallet balances and one-time gem milestones."""
    ECONOMY_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "coins": max(0, coins),
        "gems": max(0, gems),
        "gem_milestones": gem_milestones,
    }
    temporary_path = ECONOMY_PATH.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_path.replace(ECONOMY_PATH)


def load_economy() -> dict[str, Any]:
    """Load wallet data, returning starter balances for new players."""
    if not ECONOMY_PATH.exists():
        return {"coins": 120, "gems": 2, "gem_milestones": []}
    try:
        payload = json.loads(ECONOMY_PATH.read_text(encoding="utf-8"))
        return {
            "coins": max(0, int(payload.get("coins", 120))),
            "gems": max(0, int(payload.get("gems", 2))),
            "gem_milestones": payload.get("gem_milestones", []),
        }
    except (OSError, ValueError, TypeError):
        return {"coins": 120, "gems": 2, "gem_milestones": []}
