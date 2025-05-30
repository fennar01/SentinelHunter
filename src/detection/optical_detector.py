"""
optical_detector.py
Simulate optical detection events for SentinelHunter mesh.
"""
import argparse
import random
import time
import json

def simulate_optical_detection(prob=0.1):
    """Simulate an optical detection event with given probability."""
    if random.random() < prob:
        return {
            "event": "optical_rogue_sat_detected",
            "ts": time.time(),
            "confidence": random.choice(["low", "medium", "high"]),
            "ra": random.uniform(0, 360),
            "dec": random.uniform(-90, 90),
            "mag": random.uniform(6, 12),
        }
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate optical detection events.")
    parser.add_argument('--prob', type=float, default=0.1, help='Probability of detection per call')
    parser.add_argument('--n', type=int, default=10, help='Number of simulation steps')
    args = parser.parse_args()
    for _ in range(args.n):
        event = simulate_optical_detection(args.prob)
        if event:
            print(json.dumps(event))
        time.sleep(1) 