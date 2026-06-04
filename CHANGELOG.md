# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog, and version numbers follow Semantic Versioning.

## [Unreleased]

### Added
- GitHub Actions CI workflow for pytest, package build, and twine validation.
- Repository release policy and semantic versioning guidance.

### Changed
- README aligned with current packaged module usage and distribution scope.

## [0.2.0] - 2026-06-04

### Added
- Packaged `src/iack/` distribution with validated build artifacts.
- Documented import-based package usage.

### Validated
- `python -m build`
- `python -m twine check dist/*`
- `pytest` passing locally
