# CodePaws — Ecosystem Integration

Status: planning document; desktop packaging and game features must be verified independently.

## Build and release boundaries
- Keep the desktop client source and packaging instructions reproducible.
- Treat platform installers as release artifacts only after CI build and smoke tests pass.
- Keep save data separate from application binaries and document backup/reset behavior.
- Do not collect account or telemetry data without clear disclosure and controls.

## Next tasks
1. Add a minimal desktop startup smoke test.
2. Document save-game location and backup behavior per OS.
3. Verify packaged builds on Windows, macOS and Linux before claiming support.
4. Track gameplay features separately from packaging milestones.