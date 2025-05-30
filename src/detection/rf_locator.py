"""
rf_locator.py
Estimate bearing using TDOA and Doppler. Simulate RF signals and noise for multiple sources.
SentinelHunter Detection Stack
"""
import math
import argparse
import random


def simulate_rf_signals_multi(sources, baseline, carrier_freq, velocity, noise_std=1e-8):
    """
    Simulate TDOA and Doppler measurements for multiple sources.
    sources: list of dicts with 'bearing' (deg) and 'id'
    Returns: list of dicts with tdoa, frx, ftx, id
    """
    c = 299792458
    results = []
    for src in sources:
        theta_rad = math.radians(src['bearing'])
        tdoa = (baseline / c) * math.cos(theta_rad) + random.gauss(0, noise_std)
        ftx = carrier_freq
        frx = ftx * (1 + velocity / c * math.cos(theta_rad)) + random.gauss(0, 10)
        results.append({'id': src['id'], 'tdoa': tdoa, 'frx': frx, 'ftx': ftx, 'bearing': src['bearing']})
    return results

def estimate_bearing_tdoa(tdoa, baseline, c=299792458):
    """
    Estimate bearing using TDOA (Time Difference of Arrival).
    Args:
        tdoa: Time difference of arrival (seconds)
        baseline: Distance between receivers (meters)
        c: Speed of light (m/s)
    Returns:
        Estimated bearing (degrees)
    """
    # theta = arccos(c * tdoa / baseline)
    arg = c * tdoa / baseline
    arg = max(-1.0, min(1.0, arg))
    theta_rad = math.acos(arg)
    theta_deg = math.degrees(theta_rad)
    return theta_deg

def estimate_bearing_doppler(frequency_rx, frequency_tx, velocity, carrier_frequency):
    """
    Estimate the line-of-sight angle (bearing) using Doppler shift.
    Args:
        frequency_rx: Received frequency (Hz)
        frequency_tx: Transmitted frequency (Hz)
        velocity: Relative velocity between observer and source (m/s)
        carrier_frequency: Nominal carrier frequency (Hz)
    Returns:
        Estimated angle (degrees) between velocity vector and line of sight.
    """
    c = 299792458  # Speed of light (m/s)
    doppler_shift = frequency_rx - frequency_tx
    if velocity == 0 or carrier_frequency == 0:
        raise ValueError("Velocity and carrier frequency must be nonzero.")
    cos_theta = ((frequency_rx / frequency_tx) - 1) * (c / velocity)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    theta_rad = math.acos(cos_theta)
    theta_deg = math.degrees(theta_rad)
    return theta_deg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RF Locator Multi-Source Demo")
    parser.add_argument('--simulate', action='store_true', help='Simulate RF signals for multiple sources')
    parser.add_argument('--sources', type=str, default='[{"id":0,"bearing":30},{"id":1,"bearing":60}]', help='JSON list of sources with id and bearing')
    parser.add_argument('--baseline', type=float, help='Baseline (m)', default=1000)
    parser.add_argument('--fc', type=float, help='Carrier freq (Hz)', default=437100000)
    parser.add_argument('--vel', type=float, help='Relative velocity (m/s)', default=7500)
    args = parser.parse_args()

    if args.simulate:
        import json
        sources = json.loads(args.sources)
        results = simulate_rf_signals_multi(sources, args.baseline, args.fc, args.vel)
        for res in results:
            tdoa_bearing = estimate_bearing_tdoa(res['tdoa'], args.baseline)
            doppler_bearing = estimate_bearing_doppler(res['frx'], res['ftx'], args.vel, args.fc)
            print(f"Source {res['id']}: True={res['bearing']} deg | TDOA est={tdoa_bearing:.2f} deg | Doppler est={doppler_bearing:.2f} deg")
    else:
        print("Please use --simulate for multi-source demo.")
