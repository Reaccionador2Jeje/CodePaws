"""Portable, update-safe JSON save files for CodePaws.

Player data lives outside the Git checkout so updating the application
with git pull never replaces the player's progress.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any

from .models import Pet


def _user_data_dir() -> Path:
    """Return the operating-system's per-user application data directory."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif os.environ.get("XDG_DATA_HOME"):
        base = Path(os.environ["XDG_DATA_HOME"])
    else:
        base = Path.home() / ".local" / "share"
    return base / "CodePaws"


DATA_DIR = _user_data_dir()
LEGACY_DIR = Path(__file__).resolve().parent.parent / "data"


def _data_path(filename: str) -> Path:
    """Resolve a save path and migrate an older project-local save once."""
    destination = DATA_DIR / filename
    legacy = LEGACY_DIR / filename
    if not destination.exists() and legacy.exists():
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(legacy, destination)
        except OSError:
            # Fall back to the legacy location if migration is not possible.
            return legacy
    return destination


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def save_family(pets: list[Pet], selected_pet: str | None = None) -> None:
    _write_json(_data_path("save.json"), {
        "version": 2,
        "selected_pet": selected_pet,
        "pets": [pet.to_dict() for pet in pets],
    })


def load_family() -> tuple[list[Pet], str | None]:
    path = _data_path("save.json")
    if not path.exists():
        return [], None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        allowed_pet_ids = {"python", "rust", "go", "java", "docker", "github", "gitlab", "php", "kotlin", "perl"}
        pets = [
            Pet.from_dict(item)
            for item in payload.get("pets", [])
            if item.get("pet_id") in allowed_pet_ids
        ]
        selected = payload.get("selected_pet")
        if selected not in {pet.pet_id for pet in pets}:
            selected = pets[0].pet_id if pets else None
        return pets, selected
    except (OSError, ValueError, TypeError, KeyError):
        # Keep damaged saves untouched for manual recovery.
        return [], None


def save_economy(coins: int, gems: int, gem_milestones: list[int]) -> None:
    _write_json(_data_path("economy.json"), {
        "coins": max(0, coins),
        "gems": max(0, gems),
        "gem_milestones": gem_milestones,
    })


def load_economy() -> dict[str, Any]:
    defaults = {"coins": 120, "gems": 2, "gem_milestones": []}
    path = _data_path("economy.json")
    if not path.exists():
        return defaults
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {
            "coins": max(0, int(payload.get("coins", 120))),
            "gems": max(0, int(payload.get("gems", 2))),
            "gem_milestones": payload.get("gem_milestones", []),
        }
    except (OSError, ValueError, TypeError):
        return defaults


def load_house() -> dict[str, Any]:
    defaults = {"owned_accessories": ["none"]}
    path = _data_path("house.json")
    if not path.exists():
        return defaults
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        owned = data.get("owned_accessories", ["none"])
        if not isinstance(owned, list):
            owned = ["none"]
        return {"owned_accessories": sorted(set(["none", *owned]))}
    except (OSError, ValueError, TypeError):
        return defaults


def save_house(owned_accessories: list[str]) -> None:
    _write_json(_data_path("house.json"), {
        "owned_accessories": sorted(set(["none", *owned_accessories]))
    })
