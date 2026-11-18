# 🐾 CodePaws

**Your Programming Family — A Little Home for the World of Code**

CodePaws is an open-source virtual-pet project with a full-screen terminal simulator and a playable pixel-art desktop game. Adopt programming languages that have recognized mascots, take care of them, and grow your own programming family.

## Features

- Full-screen TUI powered by [Textual](https://textual.textualize.io/).
- Desktop pixel-art virtual pet game powered by [Pygame-CE](https://pyga.me/), sharing pets and save files with the TUI.
- GitHub Actions builds downloadable Windows and Linux desktop packages and publishes them as Release assets when a `v*` tag is pushed.
- Reference-informed 48×48 pixel-art companions rendered with terminal true-color pixels.
- Mascot/logo reference index with source links and attribution notes (`docs/mascot-references.md`).
- Animated idle bobbing, blinking and care-action effects.
- Adopt 10 mascots: Python, Rust, Go, Java, Docker, GitHub, GitLab, PHP, Kotlin and Perl.
- Feed, play with, let sleep, and bathe your pets.
- Happiness, energy, hunger and cleanliness statistics.
- Pet progression: earn experience through care actions, level up, and track XP.
- Every pet has its own personality and mood description.
- Family album and pet selection.
- Three-room home: living room, bedroom and garden.
- Companions roam the room autonomously, turn toward their direction of travel, and respond to floor clicks.
- Clickable room objects invite pets to visit the sofa, bed or garden.
- Move adopted pets between rooms.
- Accessory shop with pixel cap, bow, glasses and crown.
- Owned accessories persist and can be equipped on different pets.
- Coin and gem wallet with persistent balances.
- Earn coins by caring for pets, with a short reward cooldown to prevent button-spamming.
- Earn bonus gems when your family reaches 3, 6 and 10 pets.
- Mascots have rising adoption prices; rare friends also require gems.
- Automatic JSON saves for pets, wallet, rooms and accessories.
- Keyboard shortcuts and terminal resizing support.

## Requirements

- Python 3.10 or newer
- A terminal with UTF-8 support for the TUI
- A desktop environment for the Pygame game

## Install

```bash
git clone https://github.com/Reaccionador2Jeje/CodePaws.git
cd CodePaws
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

To launch the desktop game:

```bash
python desktop_game.py
```

The TUI takes over the terminal while it is running; press **Q** to quit. In the desktop game, press **A** to open the Adoption Center, click the floor to guide your pet, and click room objects to invite it over. Press **Esc** to return home from the Adoption Center, or **Esc** from the home screen to quit.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| H | Home |
| A | Adoption Center |
| F | Family |
| Q | Quit |

## Desktop game controls

| Key | Action |
| --- | --- |
| A | Open Adoption Center |
| F / P / S / B | Feed / Play / Sleep / Bathe |
| Left / Right | Switch companion |
| 1 / 2 / 3 | Change room |
| Esc | Return from Adoption Center or quit from home |

## Builds and releases

Run the **Desktop builds and releases** workflow manually from the Actions tab to create Windows and Linux build artifacts. Pushing a tag such as `v0.9.0` runs the same builds and creates a GitHub Release containing both ZIP packages. Each workflow artifact is retained for 30 days.

## Mascot family

Only languages with an established mascot are included:

| Language / tool | Mascot |
| --- | --- |
| Python | Py |
| Rust | Ferris |
| Go | Gopher |
| Java | Duke |
| Docker | Moby |
| GitHub | Mona |
| GitLab | Tanuki |
| PHP | ElePHPant |
| Kotlin | Kodee |
| Perl | Camel |

## Project status

**Version 0.9.0-dev** — Desktop Game: a playable Pygame-CE desktop experience with autonomous pet roaming is available alongside the existing TUI. Windows and Linux packages are built by GitHub Actions; pushing a version tag such as `v0.9.0` creates a GitHub Release with downloadable builds. **Version 0.8.1** — Mascot Family: the catalog includes languages and developer tools with recognized mascots. Logo-only entries without mascots remain excluded. Player saves remain outside the Git checkout.

CodePaws is a playful open-source project. Adopt. Play. Care. Build your programming family!

Made with ❤️ and code.


## Save location

Player progress is stored outside the repository so `git pull` updates do not overwrite it. On Windows, files are saved under `%APPDATA%\\CodePaws` (typically `C:\\Users\\<you>\\AppData\\Roaming\\CodePaws`). On Linux, CodePaws uses `$XDG_DATA_HOME/CodePaws` or `~/.local/share/CodePaws`. Existing saves in the project's `data` folder are copied to the new location automatically the first time the updated app starts.
