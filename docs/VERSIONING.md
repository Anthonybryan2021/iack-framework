# Versioning Rules

IACK uses Semantic Versioning: `MAJOR.MINOR.PATCH`.

- Increment PATCH for backward-compatible bug fixes, documentation-only fixes that matter to released usage, and small internal corrections.
- Increment MINOR for backward-compatible new functionality, new validated controls, new package capabilities, or additional public APIs and commands.
- Increment MAJOR for breaking changes to package structure, public imports, command behavior, file formats, or assessment outputs that consumers rely on.

Additional rules:
- Do not bump versions for every commit; bump when preparing a release.
- Record every release in `CHANGELOG.md`.
- Pre-release labels such as `1.0.0-rc1` may be used before major public release decisions.
- Until public publication is finalized, treat version tags as controlled internal releases.
