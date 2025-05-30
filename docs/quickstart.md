# Quickstart

## Prerequisites
- Docker (for sim)
- Python 3.11+
- Node.js 18+
- GCC/Clang (for C++17)

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

# Start the GUI
$ make gui
```

See [README.md](../README.md) and [ROADMAP.md](../ROADMAP.md) for more details.
