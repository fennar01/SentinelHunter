"""
node.py
Mesh node abstraction for SentinelHunter mesh network.
Each node simulates a satellite with detection, telemetry, and mesh comms.
"""
import threading
import time
import zmq
import random
import json

class Node:
    def __init__(self, node_id, peers, detection_func=None):
        self.node_id = node_id
        self.peers = peers  # List of (host, port)
        self.detection_func = detection_func or self.default_detection
        self.ctx = zmq.Context()
        self.pub = self.ctx.socket(zmq.PUB)
        self.sub = self.ctx.socket(zmq.SUB)
        self.running = False
        self.port = 5550 + node_id
        self.pub.bind(f"tcp://*:{self.port}")
        for peer_id in peers:
            self.sub.connect(f"tcp://localhost:{5550 + peer_id}")
        self.sub.setsockopt_string(zmq.SUBSCRIBE, "")

    def default_detection(self):
        # Simulate a random detection event
        if random.random() < 0.05:
            return {"event": "rogue_sat_detected", "node": self.node_id, "ts": time.time()}
        return None

    def send_telemetry(self):
        # Simulate telemetry
        msg = json.dumps({"node": self.node_id, "telemetry": random.random(), "ts": time.time()})
        self.pub.send_string(msg)

    def run(self):
        self.running = True
        def listen():
            while self.running:
                try:
                    msg = self.sub.recv_string(flags=zmq.NOBLOCK)
                    print(f"[Node {self.node_id}] Received: {msg}")
                except zmq.Again:
                    time.sleep(0.1)
        threading.Thread(target=listen, daemon=True).start()
        while self.running:
            self.send_telemetry()
            detection = self.detection_func()
            if detection:
                self.pub.send_string(json.dumps(detection))
            time.sleep(1)

    def stop(self):
        self.running = False
        self.pub.close()
        self.sub.close()
        self.ctx.term()

if __name__ == "__main__":
    # Simulate a mesh of 3 nodes
    nodes = [Node(i, [j for j in range(3) if j != i]) for i in range(3)]
    threads = [threading.Thread(target=n.run, daemon=True) for n in nodes]
    for t in threads: t.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for n in nodes: n.stop() 