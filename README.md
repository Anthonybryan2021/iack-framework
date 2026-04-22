# I-A-C-K Framework

The I-A-C-K framework is a mathematical and AI-driven model for real-time confidentiality proxy measurement in quantum-safe cybersecurity systems.

## Purpose

This repository is the working space for a research and prototype effort focused on:
- measuring confidentiality in real time,
- modeling security-state changes with operational signals,
- and exploring AI-assisted forecasting and anomaly detection for cybersecurity defense.

## Core Idea

The framework defines a confidentiality proxy using integrity and availability signals:

- **Integrity**: breach events, modification attempts, and hash validation failures
- **Availability**: uptime, authentication success, and response stability
- **Confidentiality proxy**: a derived score based on integrity and availability
- **Efficiency**: a time-windowed measure of how consistently the system preserves the confidentiality proxy

## Current Status

This repository currently contains:
- the initial project structure,
- a starter metric computation module,
- and a working draft of the framework summary.

## Repository Structure

- `docs/` — project notes and summaries
- `src/` — source code for the framework
- `notebooks/` — exploratory analysis and prototypes
- `diagrams/` — architecture and concept diagrams
- `references/` — source material and research notes

## Running the Prototype

The starter implementation is in `src/metrics.py`.

If Python is installed, you can run it with:

```powershell
python .\src\metrics.py
```

That will print a sample output dictionary with the computed integrity, availability, confidentiality proxy, and windowed efficiency values.

## Roadmap

Planned next steps include:
- expanding the metric definitions,
- adding tests,
- building a notebook for experimentation,
- and validating the framework against synthetic and real-world security logs.

## License

This project is released under the MIT License.
