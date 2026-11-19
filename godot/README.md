# CodePaws 3D

The Godot 4 project is being developed alongside the original Python/Pygame prototype while core systems are rebuilt.

## Open the project

1. Install Godot 4.3 or newer.
2. Import the `godot/project.godot` file in the Godot Project Manager.
3. Press Play Project to run the 3D prototype.

## Current prototype

- Lightweight stylized 3D valley with a village path, pond, houses and trees.
- Third-person player controller with keyboard movement, jumping and mouse camera.
- Four procedural companion prototypes that wander around and respond to interaction.
- Pet needs: hunger, happiness, cleanliness and energy.
- Feed a nearby companion and improve its happiness by interacting with it.
- Local save/load system for player position, companion positions and companion stats.
- Compatibility renderer selected for a broad range of hardware.

## Controls

- WASD: move
- Mouse: look around
- Space: jump
- F: pet/interact with a nearby companion
- E: feed a nearby companion
- F5: save the game
- F9: load the saved game
- Esc: release mouse; click to capture it again

Save data is stored locally at `user://codepaws_save.json`.

## Development status

This is an early playable prototype, not a finished open world. The current companions still use procedural placeholder meshes. Custom mascot models, animation, mobile touch controls, larger explorable areas, interior spaces, and Steam packaging remain future milestones.
