"""
rf_locator.py
Estimate bearing using TDOA and Doppler. Simulate RF signals and noise.
SentinelHunter Detection Stack
"""
import math
import argparse
import random

def simulate_rf_signals(true_bearing_deg, baseline, carrier_freq, velocity, noise_std=1e-8):
    """
    Simulate TDOA and Doppler measurements for a given true bearing, with noise.
    Returns: tdoa (s), frx (Hz), ftx (Hz)
    """
    c = 299792458
    # Simulate TDOA: tdoa = (baseline/c) * cos(theta)
    theta_rad = math.radians(true_bearing_deg)
    tdoa = (baseline / c) * math.cos(theta_rad)
    tdoa += random.gauss(0, noise_std)
    # Simulate Doppler: frx = ftx * (1 + v/c * cos(theta))
    ftx = carrier_freq
    frx = ftx * (1 + velocity / c * math.cos(theta_rad))
    frx += random.gauss(0, 10)  # 10 Hz noise
    return tdoa, frx, ftx

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
    parser = argparse.ArgumentParser(description="RF Locator Demo")
    parser.add_argument('--simulate', action='store_true', help='Simulate RF signals')
    parser.add_argument('--bearing', type=float, default=30.0, help='True bearing (deg, for simulation)')
    parser.add_argument('--baseline', type=float, help='Baseline (m)', default=1000)
    parser.add_argument('--fc', type=float, help='Carrier freq (Hz)', default=437100000)
    parser.add_argument('--vel', type=float, help='Relative velocity (m/s)', default=7500)
    parser.add_argument('--tdoa', type=float, help='TDOA (s)')
    parser.add_argument('--frx', type=float, help='Received freq (Hz)')
    parser.add_argument('--ftx', type=float, help='Transmitted freq (Hz)')
    args = parser.parse_args()

    if args.simulate:
        tdoa, frx, ftx = simulate_rf_signals(args.bearing, args.baseline, args.fc, args.vel)
        print(f"Simulated: TDOA={tdoa:.2e} s, frx={frx:.2f} Hz, ftx={ftx:.2f} Hz")
    else:
        tdoa = args.tdoa
        frx = args.frx
        ftx = args.ftx
        if tdoa is None or frx is None or ftx is None:
            parser.error('Must provide --tdoa, --frx, and --ftx if not simulating.')

    tdoa_bearing = estimate_bearing_tdoa(tdoa, args.baseline)
    doppler_bearing = estimate_bearing_doppler(frx, ftx, args.vel, args.fc)
    print(f"TDOA estimated bearing: {tdoa_bearing:.2f} deg")
    print(f"Doppler estimated bearing: {doppler_bearing:.2f} deg")
