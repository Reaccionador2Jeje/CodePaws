# CodePaws Desktop

CodePaws Desktop is the new cross-platform desktop client built with Tauri 2, Vite and Three.js. The original Python/Pygame and Godot prototypes remain in the repository as references while this client is developed.

## Requirements for local development

- Node.js 20 or newer
- Rust stable toolchain
- Tauri 2 platform prerequisites: https://v2.tauri.app/start/prerequisites/

## Run

From this directory:

```sh
npm install
npm run tauri -- dev
```

## Build

```sh
npm run tauri -- build
```

GitHub Actions builds Windows NSIS setup executables, macOS DMG images, and Linux DEB/RPM packages. The current scene is an early playable 3D foundation; save data and game systems are being expanded incrementally.
