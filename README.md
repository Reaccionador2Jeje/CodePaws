# 🐾 CodePaws

**Your Programming Family — A Little Home for the World of Code**

CodePaws is an open-source virtual-pet game about adopting programming mascots, caring for them and exploring a colorful world together.

## Current direction: CodePaws Desktop

The active desktop direction is a cross-platform 3D game built with **Tauri 2 + Three.js**. The desktop client lives in [`desktop/`](desktop/), while the original Python/Pygame and Godot prototypes remain available as project history and references.

The goal is to distribute native desktop installers through GitHub Releases:

- **Windows:** NSIS setup executable (`.exe`)
- **macOS:** disk image (`.dmg`)
- **Debian / Ubuntu:** package (`.deb`)
- **Fedora / RPM-based Linux:** package (`.rpm`)

GitHub Actions builds each platform on its matching hosted runner. No local game-engine installation is needed to produce release builds.

## Desktop client development

See [`desktop/README.md`](desktop/README.md) for setup instructions.

Requirements for local development:
- Node.js 20+
- Rust stable
- Tauri 2 platform prerequisites

Run from the `desktop/` directory:

```sh
npm install
npm run tauri -- dev
```

## Game vision

CodePaws is planned as a cozy, stylized 3D open-world pet adventure featuring:

- A player home with an explorable interior and garden.
- A lively town with streets, a plaza, shops and friendly characters.
- Large mountain ranges, forests, lakes and hidden places.
- Ten programming mascots: Py, Ferris, Gopher, Duke, Moby, Mona, Tanuki, ElePHPant, Kodee and Camel.
- Pet care: hunger, energy, cleanliness, happiness, experience and levels.
- Adoption, accessories, rooms, coins, gems and persistent saves.

The current Three.js scene is an early playable foundation, not the finished open world. Features will be added in small, testable stages.

## Legacy prototypes

- `codepaws/` — original Python virtual-pet systems and Pygame interface.
- `godot/` — earlier Godot 4 3D experiment, paused while the Tauri desktop client is developed.

These folders are intentionally retained; the new desktop client does not delete or overwrite them.

## GitHub Actions builds

Open the **Actions** tab and run **CodePaws Desktop builds** with **Run workflow** to create downloadable test installers. Pushing a tag such as `v1.0.0` builds all four package formats and creates a GitHub Release.

Each build is produced on its native operating-system runner. Build artifacts are retained for 30 days. The first builds still need runtime testing on Windows, macOS and Linux; package generation alone does not certify compatibility.

## Project status

**1.0.0-dev — Desktop foundation:** Tauri 2 shell, Three.js 3D valley prototype, basic third-person movement, initial pet family display and cross-platform GitHub Actions packaging pipeline.

CodePaws is an open-source project. Adopt. Explore. Care. Build your programming family!

Made with ❤️ and code.
