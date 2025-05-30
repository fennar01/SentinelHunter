# SentinelHunter

SentinelHunter is a mesh-based mission software stack for deployment on existing satellite constellations (e.g., Iridium, Starlink, military) to detect and track rogue 'killer' satellites using RF, Doppler, and optical signatures. The system supports multi-satellite collaboration, real-time mesh networking, and a unified ground operator GUI.

## Architecture
- **Node:** Each satellite runs a lightweight SentinelHunter node, capable of local detection, telemetry, and mesh communication.
- **Mesh Network:** Nodes communicate and share detection/telemetry data using a mesh protocol (simulated with ZeroMQ for development).
- **Unified GUI:** A ground operator console visualizes the entire mesh, real-time detection events, and allows network control.
- **Simulation:** The system can be run in a fully simulated mode on the ground, with multiple virtual satellites.

## Features
- Real-time detection of rogue satellites using RF, Doppler, and (future) optical signatures
- Mesh networking for distributed detection and data fusion
- Unified GUI for constellation-wide situational awareness and control
- Modular architecture for easy extension to new constellations or detection methods
- Simulation tools for proof-of-concept and development

## Repository Structure
- `src/flight` – C++17 flight core (attitude, telemetry)
- `src/detection` – Python sensor-fusion algorithms (RF, Doppler, TDOA, simulation)
- `src/mesh` – Mesh node abstraction and network protocol (ZeroMQ)
- `src/gui` – React + Electron operator console (CesiumJS visualization)
- `sim` – Simulator with STK-compatible propagator
- `tests` – Unit and integration tests
- `docs` – Documentation and API references

## Quickstart
See [docs/quickstart.md](docs/quickstart.md) for 5-minute build and run instructions.

## Roadmap
See [ROADMAP.md](ROADMAP.md) for current and planned features.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose new features, add roadmap items, and contribute code.
