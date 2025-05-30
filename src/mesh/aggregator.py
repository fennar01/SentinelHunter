"""
aggregator.py
Aggregates mesh node telemetry and detection events for GUI visualization.
Subscribes to all node PUB sockets and writes mesh_events.json.
"""
import zmq
import json
import time
import threading
import random

N_NODES = 3
OUTPUT_PATH = 'src/gui/data/mesh_events.json'

# For demo: assign each node a fixed orbit position
NODE_POSITIONS = [
    {"id": 0, "lon": 0, "lat": 0, "alt": 400000},
    {"id": 1, "lon": 10, "lat": 10, "alt": 400000},
    {"id": 2, "lon": 20, "lat": 20, "alt": 400000},
]

def aggregator():
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    for i in range(N_NODES):
        sub.connect(f"tcp://localhost:{5550 + i}")
    sub.setsockopt_string(zmq.SUBSCRIBE, "")
    detections = []
    while True:
        try:
            msg = sub.recv_string(flags=zmq.NOBLOCK)
            try:
                data = json.loads(msg)
                if isinstance(data, dict) and data.get("event") == "rogue_sat_detected":
                    # Attach node position for GUI
                    node_id = data["node"]
                    pos = next((n for n in NODE_POSITIONS if n["id"] == node_id), None)
                    if pos:
                        detections.append({"node": node_id, "lon": pos["lon"], "lat": pos["lat"], "alt": pos["alt"], "ts": data["ts"]})
            except Exception:
                pass
        except zmq.Again:
            pass
        # Write mesh_events.json every second
        with open(OUTPUT_PATH, 'w') as f:
            json.dump({"nodes": NODE_POSITIONS, "detections": detections[-10:]}, f)
        time.sleep(1)

if __name__ == "__main__":
    print("Starting mesh aggregator...")
    aggregator() 