# 🐾 CodePaws

**Your Programming Family — A Little Home for the World of Code**

CodePaws is a full-screen terminal virtual-pet simulator. Adopt mascots inspired by programming languages and developer tools, take care of them, and grow your own programming family.

## Features

- Full-screen TUI powered by [Textual](https://textual.textualize.io/).
- Real 48×48 pixel-art mascots rendered with terminal true-color pixels.
- Animated idle bobbing, blinking and care-action effects.
- Adopt 16 mascots: Python, Rust, Go, Java, Docker, GitHub, GitLab, PHP, JavaScript, TypeScript, Ruby, C, C++, Kotlin, Swift and Perl.
- Feed, play with, let sleep, and bathe your pets.
- Happiness, energy, hunger and cleanliness statistics.
- Pet progression: earn experience through care actions, level up, and track XP.
- Every pet has its own personality and mood description.
- Family album and pet selection.
- Three-room home: living room, bedroom and garden.
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
- A terminal with UTF-8 support

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

The application takes over the terminal while it is running. Press **Q** to quit and return to your shell.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| H | Home |
| A | Adoption Center |
| F | Family |
| Q | Quit |

## Mascot family

| Technology | Mascot |
| --- | --- |
| Python | Py |
| Rust | Ferris |
| Go | Gopher |
| Java | Duke |
| Docker | Moby |
| GitHub | Octocat |
| GitLab | Tanuki |
| PHP | ElePHPant |
| JavaScript | Javie |
| TypeScript | Tessa |
| Ruby | Ruby |
| C | Cee |
| C++ | PlusPlus |
| Kotlin | Koko |
| Swift | Swiftie |
| Perl | Camel |

## Project status

**Version 0.6.3** — Mascot Art Refresh: all 16 companions have friendlier, more distinctive pixel-art designs. Official mascot characters are represented as fan-made interpretations; technologies without an official mascot use original CodePaws companions. Player saves remain outside the Git checkout.

CodePaws is a playful open-source project. Adopt. Play. Care. Build your programming family!

Made with ❤️ and code.


## Save location

Player progress is stored outside the repository so `git pull` updates do not overwrite it. On Windows, files are saved under `%APPDATA%\\CodePaws` (typically `C:\\Users\\<you>\\AppData\\Roaming\\CodePaws`). On Linux, CodePaws uses `$XDG_DATA_HOME/CodePaws` or `~/.local/share/CodePaws`. Existing saves in the project's `data` folder are copied to the new location automatically the first time the updated app starts.
