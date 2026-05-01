# IACK Framework

> An open cybersecurity framework in active early-stage development for structuring and validating security-related metrics in a clear, reproducible, and academically serious way.

![Status](https://img.shields.io/badge/status-active%20development-blue)
![Python](https://img.shields.io/badge/python-3.13+-blue)
![Tests](https://img.shields.io/badge/tests-unittest-green)

## Overview

IACK Framework is an open, research-oriented cybersecurity project focused on building a structured foundation for security metric development, validation, and interpretation.

The project is being developed as a technical and academic initiative rather than a finished product. Its purpose is to evolve into a serious framework for measurable security analysis, with emphasis on clarity, reproducibility, integrity, and long-term research value.

At its current stage, IACK is in foundation-building mode. The repository includes early project structure, initial metric logic, and validation work that is intended to support future architectural growth, technical refinement, and academic collaboration.

## Project Vision

The vision of IACK is to build a framework that can support disciplined work around security metrics in a way that is technically meaningful and academically useful.

Rather than presenting broad claims too early, IACK is being developed step by step as a base for:
- defining and refining security-oriented metrics,
- validating how those metrics are computed,
- structuring a framework that can mature through transparent development,
- and creating something that may eventually contribute academic value, including for future students, researchers, and practitioners.

The long-term aspiration is for IACK to become a principled and well-documented body of work that reflects integrity, rectitude, and serious technical effort.

## Current Status

**Project stage:** Active early-stage development

At this time, IACK should be understood as an evolving framework, not a complete production-ready platform.

Current repository progress includes:
- early repository organization,
- initial metrics-related code and validation logic,
- unit testing for `compute_iack_metrics`,
- pull-request-based iteration,
- and the beginning of a more structured development workflow.

This is the stage where architecture, scope, documentation, and contribution pathways are being intentionally shaped.

## Current Capabilities

The repository currently supports early validation around metrics behavior, including:
- returning expected keys from `compute_iack_metrics`,
- checking that metric values are numeric,
- validating error handling for invalid inputs,
- and confirming placeholder default metric values through unit tests.

These capabilities are still foundational, but they establish an important base for future expansion.

## Guiding Principles

IACK is being developed with a small set of guiding principles:

- **Integrity** — the project should grow honestly, without overstating its maturity.
- **Transparency** — assumptions, limitations, and status should be clearly communicated.
- **Rectitude** — the work should remain disciplined, principled, and purposeful.
- **Reproducibility** — metric logic and validation should be understandable and testable.
- **Collaboration** — the framework should become easier for serious contributors to review, improve, and extend.

## Repository Structure

> The exact structure may evolve as the project matures.

A typical current layout includes:

```text
iack-framework/
+-- src/
¦   +-- metrics.py
+-- tests/
¦   +-- test_metrics.py
+-- README.md
+-- ...
```

Key areas:
- `src/` — source code for the framework
- `tests/` — unit tests and validation logic
- `README.md` — project overview, status, and collaboration entry point

As the project grows, this structure may expand to include architecture notes, roadmap files, contribution guides, documentation, and CI workflows.

## Getting Started

### Requirements

- Python 3.13 or compatible version
- Git
- A local clone of the repository

### Clone the repository

```bash
git clone https://github.com/Anthonybryan2021/iack-framework.git
cd iack-framework
```

### Run the tests

```bash
python -m unittest discover -s tests
```

If the tests pass, you should see the current validation suite complete successfully.

## Development Approach

IACK is currently being developed in a disciplined incremental manner:
- define a small technical objective,
- implement or refine the relevant logic,
- validate behavior with tests,
- review changes through pull requests,
- and improve documentation as the framework becomes clearer.

This approach is intentional. The goal is not to move quickly at the expense of rigor, but to let the framework mature in a way that remains coherent and credible.

## Roadmap

The roadmap is still evolving, but the current direction can be understood in three phases.

### Phase 1 — Foundation
- clarify repository structure,
- strengthen README and project documentation,
- validate baseline metric behavior,
- and establish a more consistent development workflow.

### Phase 2 — Architecture and Validation
- define a clearer architectural model for IACK,
- expand metrics design and validation logic,
- improve testing coverage,
- and introduce CI support for automated test execution.

### Phase 3 — Collaboration and Research Maturity
- prepare the repository for broader technical and academic collaboration,
- improve documentation for contributors,
- explore stronger experimental and analytical grounding,
- and position the framework for more serious research-oriented development.

## Contribution Intent

At this stage, meaningful contributions may include:
- architectural feedback,
- review of metric design and assumptions,
- testing and validation improvements,
- documentation refinement,
- repository organization,
- and academic or research-oriented guidance.

The project especially welcomes thoughtful contributors who value serious technical work, humility in framing early-stage systems, and integrity in how ideas are developed.

## How to Contribute

If you are interested in contributing:
1. Review the README and current repository structure.
2. Open an issue or start a discussion around a concrete suggestion.
3. Fork the repository or work from a branch if collaboration access is granted.
4. Submit focused pull requests with clear explanations.
5. Keep changes aligned with the project’s technical and ethical direction.

As the repository matures, contribution guidelines will become more formalized in a dedicated `CONTRIBUTING.md` file.

## Collaboration

IACK is open to serious collaboration, especially where there is alignment around:
- cybersecurity research,
- security metric design,
- framework architecture,
- transparent technical development,
- and long-term academic value.

The project is particularly interested in collaboration that helps strengthen both the technical rigor and the intellectual seriousness of the framework.

## Limitations

This repository is still early-stage.

That means:
- the architecture is still evolving,
- metric design is still being refined,
- current outputs may include placeholder values,
- and documentation is still catching up with the project’s intended direction.

These limitations are acknowledged openly so that the framework can grow with credibility.

## Why This Project Exists

Many security ideas are discussed at a high level, but fewer are developed in a way that is structured, testable, and reproducible from an early stage.

IACK exists to explore a more disciplined path: building a framework carefully, validating it incrementally, and allowing its direction to mature through principled technical work instead of inflated claims.

## Academic Orientation

Although IACK is still early, part of its long-term aspiration is to become useful not only as a technical repository, but also as a piece of work with academic value.

This includes the hope that it may eventually support:
- deeper technical study,
- clearer security-metric reasoning,
- collaborative research discussion,
- and future learners or researchers who want to build on an honest and well-structured foundation.

## License

This project is licensed under the Apache License 2.0.

Apache 2.0 was chosen to support open collaboration, broad reuse, and clearer legal protection for contributors and downstream users, including an explicit patent grant.

See the [LICENSE](LICENSE) file for full terms.

## Contact

For collaboration, academic discussion, or technical feedback, please open an issue or reach out through the appropriate project contact channel.

---

**IACK Framework** is being built patiently, seriously, and with the conviction that useful work should be clear, testable, and intellectually honest from the beginning.
