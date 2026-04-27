# I-A-C-K Framework

The I-A-C-K Framework is a mathematical and AI-assisted research prototype for real-time confidentiality proxy measurement in cybersecurity systems. It explores how operational security signals can be combined into a practical, measurable proxy for confidentiality when direct measurement is difficult or impossible. [file:396]

## Overview

This repository is the working space for an early-stage framework focused on:

- measuring confidentiality through indirect but observable system behavior,
- modeling security-state changes using integrity and availability indicators,
- and supporting future AI-assisted forecasting, anomaly detection, and decision support for cyber defense. [file:396]

The current implementation is intentionally lightweight. It provides a baseline structure for the project, a starter metrics module, and a first set of unit tests that establish an initial testing foundation for future development. [file:396][file:509]

## Core Concept

The framework treats confidentiality as a derived security property that can be approximated through related operational signals.

The current conceptual model uses four core outputs:

- **Integrity** — signals related to trustworthiness of data and system state, such as breach events, modification attempts, or validation failures. [file:396]
- **Availability** — signals related to system reliability and accessibility, such as uptime, authentication success, and response stability. [file:396]
- **Confidentiality proxy** — a derived score based on the relationship between integrity and availability indicators. [file:396]
- **Windowed efficiency** — a time-based measure of how consistently the system preserves the confidentiality proxy across a defined interval. [file:396]

This framing is meant as a prototype foundation rather than a finished security model. The formulas, assumptions, and operational definitions will evolve as the project matures. [file:396]
## Project Principles

The I-A-C-K Framework is guided by a set of principles intended to keep the project scientifically credible, ethically grounded, and practically relevant.

- **Transparency** — openly document assumptions, methodologies, and data sources.
- **Reproducibility** — validate the framework through reproducible experiments, testing, and peer-oriented review.
- **Ethical AI** — prioritize fairness, accountability, and respect for privacy in AI-assisted security analysis.
- **Open collaboration** — encourage constructive feedback and diverse perspectives from researchers, practitioners, and contributors.
- **Standards alignment** — aim to align the framework with recognized cybersecurity practices and quantum-safe security considerations.
- **Iterative improvement** — refine the model continuously as evidence, threats, and technologies evolve.
- **Honest communication** — clearly state the framework’s current capabilities, assumptions, and limitations.

These principles are intended to help ensure that the project develops as a trustworthy research and prototype effort rather than only as a technical experiment.

## Repository Structure

The repository currently centers on these main areas:

- `docs/` — project notes, summaries, and supporting writeups.
- `src/` — source code for the prototype framework and metric computations.
- `tests/` — baseline unit tests for the starter metrics module. [file:509]

If additional research folders such as notebooks, diagrams, or references are added later, they can be documented here once they are present in the repository structure. [file:396][file:510]

## Current Status

At this stage, the repository contains:

- the initial project structure,
- a starter metric computation module in `src/metrics.py`,
- a working draft of the framework description,
- and passing unit tests for the baseline metrics prototype. [file:396][file:509]

The current metrics implementation exposes a `compute_iack_metrics()` function that returns a dictionary with the framework’s baseline outputs. The present version should be treated as a scaffold for further research, refinement, and validation rather than a production-ready security engine. [file:507][file:509]

## Getting Started

### Requirements

- Python 3.x
- A local environment capable of running standard library `unittest` tests

### Run the tests

From the repository root, run:

```powershell
python -m unittest discover -s tests -v
```

The current baseline test suite checks that the starter metrics function:

- returns the expected keys,
- returns numeric values,
- raises an error for invalid `total_events`,
- and raises an error for invalid `window_size`. [file:509]

## Prototype Usage

The starter implementation lives in:

```text
src/metrics.py
```

The current baseline interface is centered on:

```python
compute_iack_metrics(total_events=1, window_size=1)
```

It returns a dictionary with the following keys:

- `integrity`
- `availability`
- `confidentiality_proxy`
- `windowed_efficiency` [file:507]

Example:

```python
from src.metrics import compute_iack_metrics

result = compute_iack_metrics()
print(result)
```

## Roadmap

Planned next steps include:

- expanding the metric definitions beyond placeholder values,
- introducing more realistic confidentiality proxy logic,
- adding richer test coverage for edge cases and expected ranges,
- building notebooks or experiments for model exploration,
- and validating the framework against synthetic and real-world security telemetry. [file:396][file:509]

## Research Direction

This repository is best understood as a research and prototyping effort at the intersection of:

- cybersecurity measurement,
- mathematical security modeling,
- operational telemetry,
- and AI-assisted analysis. [file:396]

As the framework evolves, future work may include better event modeling, weighted scoring, time-series analysis, anomaly detection, and domain validation against real security workflows. [file:396]

## License

This project is released under the MIT License. [file:396]

## Development

### Local testing

This project uses `pytest` for automated tests.

Run the test suite locally with:

```powershell
python -m pytest -q
```

### Continuous integration

GitHub Actions runs the test suite automatically on:
- pushes to `main`
- pull requests targeting `main`

### Notes

At the moment, this repository does not use `requirements.txt`, `pyproject.toml`, or `setup.py`, so tests run directly against the source tree.
