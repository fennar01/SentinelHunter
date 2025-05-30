# .devcontainer/Dockerfile
FROM debian:stable-slim

RUN apt-get update && \
    apt-get install -y gcc clang python3.11 python3.11-venv python3-pip nodejs npm curl git && \
    npm install -g npm@9 && \
    npm install -g cesium

# Install CesiumJS assets (placeholder)
RUN mkdir -p /cesium-assets

CMD ["bash"]
