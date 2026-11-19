---
version: alpha
name: "CodePaws Desktop"
description: "A cozy, playful 3D desktop pet adventure inspired by a bright mountain valley and a welcoming little town."
colors:
  ink: "#172A32"
  forest: "#477C58"
  meadow: "#82AD72"
  sky: "#A8D5DC"
  cream: "#F5E8C9"
  honey: "#F0D99E"
  coral: "#C9785C"
  glass: "#193D3C"
typography:
  display:
    fontFamily: "Manrope, DM Sans, system-ui, sans-serif"
  sans:
    fontFamily: "DM Sans, system-ui, sans-serif"
  utility:
    fontFamily: "ui-monospace, SFMono-Regular, monospace"
rounded:
  card: "18px"
  control: "10px"
  badge: "999px"
spacing:
  panel-inset: "14px"
  desktop-gutter: "42px"
components:
  hud-panel: {}
  action-button: {}
  status-card: {}
omitted:
  - section: charts
    reason: "The game HUD has no charts."
  - section: data-tables
    reason: "The game HUD has no tabular data."
---

# CodePaws Desktop Design System

## Overview

### Creative North Star

A welcoming mountain-town diorama: the visual language of a hand-crafted family adventure game, with soft daylight, leafy greens, warm timber, painted plaster and small moments of honey-colored light. The 3D world is the hero; interface panels should feel like lightweight field notes layered over the landscape.

### Product context and register

- **Audience and primary job:** Players exploring a 3D world and caring for a family of programming mascots.
- **Target market(s) and evidence:** International desktop audience; interface copy is currently Spanish-first with simple language.
- **Locale(s) and language policy:** Spanish UI for the initial prototype; keep copy short and avoid text baked into 3D assets.
- **Usage scene:** Desktop game window, keyboard movement and mouse camera control.
- **Register:** Hybrid; expressive game world, quiet and legible HUD.
- **Memorable signature:** A translucent forest-green companion card with a warm cream snack action.
- **Restraint:** Keep the central world unobstructed; HUD panels should not compete with scenery.
- **Anti-references:** Dense productivity dashboards, neon cyberpunk HUDs, photorealistic military interfaces, generic mobile-game energy meters.
- **Token ownership/runtime mapping:** This file records the palette; runtime values are currently implemented in `desktop/src/style.css` and `desktop/src/main.js`. Keep those values aligned when the visual system changes.

## Colors

The environment owns the broad palette: sky blue, meadow green, forest foliage and warm path stone. The interface uses deep blue-green for readable translucent surfaces, cream for primary text and honey for the one high-value action. Coral is reserved for architectural accents, not warnings.

## Typography

Manrope carries short display headlines and pet names. DM Sans handles controls, descriptions and HUD copy. System sans-serif fallbacks keep the interface usable offline. Utility labels are compact uppercase with expanded tracking; avoid long all-caps sentences.

## Layout

The 3D canvas fills the window. The top bar is a narrow orientation strip, the left welcome panel is contextual rather than navigational, the companion card sits at the lower right, and movement hints stay in a bottom rail. On smaller desktop windows, panels move inward and the scene remains the dominant surface.

## Elevation & Depth

Depth comes from the 3D scene, atmospheric fog and translucent HUD panels. Use restrained blur and soft shadows only on floating HUD surfaces. Avoid stacking multiple opaque cards over the center of the world.

## Shapes

HUD surfaces use generous 18px corners; interactive controls use 10px corners. The world itself uses softened low-poly silhouettes, rounded tree crowns and simple house volumes. Avoid sharp sci-fi bevels.

## Components

### Foundational visual states

Buttons need visible hover, pressed and keyboard-focus states. Status messages use the toast near the bottom center. Disabled actions must remain legible and must not appear clickable.

### Buttons and actions

The companion-care action is the warm cream button. It uses a direct verb and a short label. Secondary actions remain quiet and transparent.

### Navigation and data display

The top bar identifies the game and current region. The companion card identifies the selected mascot. Movement hints are always visible without taking focus away from the world.

### Forms and overlays

The prototype uses no forms or modal overlays. Future adoption and inventory screens should preserve the same forest/cream palette and keep the 3D world visible where practical.

### Iconography

Use familiar Unicode symbols and mascot emoji only for prototype affordances. Replace with a consistent original icon set before release; never rely on color alone to communicate state.

### Motion

Mascots bob gently and camera movement follows deliberate pointer drag. UI transitions are brief and subtle. Respect reduced-motion preferences for interface animation and provide a camera-sensitivity setting before release.

### Content and data visualization

Use friendly, concise Spanish. Prefer “Dar snack”, “Explorar” and “Conocer amigos” over technical terms. Avoid fake numeric indicators; only show needs and progress when backed by real game state.

## Do's and Don'ts

- **Do:** Let the 3D valley remain the main attraction.
- **Do:** Use warm, readable HUD surfaces with strong contrast.
- **Don't:** Cover the player or companion with decorative panels.
- **Don't:** imply that unfinished prototype systems are already implemented.

## Mascot identity and canon

The companion roster represents real programming languages, developer tools, platforms and operating systems. Do not replace these identities with unrelated generic animal pets or present original designs as official mascots.

### Canonical roster

| Mascot | Represents | Category |
|---|---|---|
| Py (paired blue/yellow snakes) | Python | Language |
| Ferris (crab) | Rust | Language |
| Gopher (gopher) | Go | Language |
| ElePHPant (elephant) | PHP | Language |
| Duke | Java | Language |
| Camel | Perl | Language |
| Camelia (butterfly) | Raku | Language |
| Zero and Ziguana (iguanas) | Zig | Language |
| Dash (hummingbird) | Dart | Language |
| Crystal (faceted crystal) | Crystal | Language |
| Moby Dock (whale) | Docker | Tool |
| Mona / Octocat | GitHub | Platform |
| Tanuki | GitLab | Platform |
| Tux (penguin) | Linux | Operating system |
| Slonik (elephant) | PostgreSQL | Tool |
| Sakila (dolphin) | MySQL | Tool |
| GNU (gnu) | GNU | System |
| Kodee | Kotlin | Language |

Use original, game-ready 3D interpretations that clearly communicate each mascot's recognizable silhouette. Keep official names and associations accurate. The roster may grow, but each new companion must be tied to a real language, tool, platform or system and its known mascot where one exists.
