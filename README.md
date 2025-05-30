# SentinelHunter

[![Build Status](https://github.com/your-org/SentinelHunter/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/SentinelHunter/actions)
[![Coverage Status](https://coveralls.io/repos/github/your-org/SentinelHunter/badge.svg?branch=main)](https://coveralls.io/github/your-org/SentinelHunter?branch=main)

SentinelHunter is a mission software stack for micro-satellites to detect and track rogue 'killer' satellites using RF, Doppler, and optical signatures.

## Repository Structure
- `src/flight` – C++17 flight core
- `src/detection` – Python sensor-fusion algorithms
- `src/gui` – React + Electron operator console
- `sim` – Simulator with STK-compatible propagator
- `tests` – Unit and integration tests
- `docs` – Documentation and API references

## Quickstart
See [docs/quickstart.md](docs/quickstart.md) for 5-minute build and run instructions.

## Roadmap
See [ROADMAP.md](ROADMAP.md) for current epics and status.
