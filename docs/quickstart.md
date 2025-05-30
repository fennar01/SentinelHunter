# Quickstart

## Prerequisites
- Docker (for sim)
- Python 3.11+
- Node.js 18+
- GCC/Clang (for C++17)
- [ZeroMQ Python bindings](https://pypi.org/project/pyzmq/) (`pip install pyzmq`)

## Build and Run

```sh
# Clone the repo
$ git clone <repo-url>
$ cd killerSatFinder

# Install pre-commit hooks
$ pre-commit install

# Build all components
$ make build

# Run tests
$ make test

# Lint all code
$ make lint

# Run the simulator
$ make sim

# Start a mesh simulation (3 nodes)
$ python src/mesh/node.py

# In a separate terminal, run the aggregator for event fusion and GUI visualization
$ python src/mesh/aggregator.py

# Start the GUI (in a separate terminal)
$ make gui
```

The GUI will connect to the mesh and visualize all nodes, detection events, and high-confidence fusion events in real time.

See [README.md](../README.md) and [ROADMAP.md](../ROADMAP.md) for more details.

All initial roadmap epics are complete. You can now add new features or iterate on the existing modules.
