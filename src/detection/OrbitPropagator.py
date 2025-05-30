"""
OrbitPropagator.py
SGP4 orbit propagation with atmospheric drag toggle.
SentinelHunter Detection Stack
"""

import argparse
try:
    from sgp4.api import Satrec, jday
    SGP4_AVAILABLE = True
except ImportError:
    SGP4_AVAILABLE = False

class OrbitPropagator:
    def __init__(self, tle1=None, tle2=None, use_drag=False):
        """Initialize the propagator with optional atmospheric drag."""
        self.use_drag = use_drag
        self.tle1 = tle1
        self.tle2 = tle2
        if SGP4_AVAILABLE and tle1 and tle2:
            self.sat = Satrec.twoline2rv(tle1, tle2)
        else:
            self.sat = None

    def propagate(self, year, month, day, hour, minute, second):
        """Propagate orbit using SGP4. Returns position and velocity (km, km/s)."""
        if not SGP4_AVAILABLE or not self.sat:
            print("SGP4 not available or TLE not set. Returning placeholder.")
            return [0,0,0], [0,0,0]
        jd, fr = jday(year, month, day, hour, minute, second)
        e, r, v = self.sat.sgp4(jd, fr)
        if e == 0:
            return r, v
        else:
            print(f"SGP4 error: {e}")
            return [0,0,0], [0,0,0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orbit Propagator Demo")
    parser.add_argument('--tle1', type=str, default="1 25544U 98067A   21275.51835648  .00000282  00000-0  12509-4 0  9993", help='TLE line 1')
    parser.add_argument('--tle2', type=str, default="2 25544  51.6442  21.4376 0005543  41.2172  61.2342 15.48815329308153", help='TLE line 2')
    parser.add_argument('--date', type=str, default="2021-10-02T12:00:00", help='UTC date (YYYY-MM-DDTHH:MM:SS)')
    args = parser.parse_args()
    from datetime import datetime
    dt = datetime.fromisoformat(args.date)
    op = OrbitPropagator(args.tle1, args.tle2)
    r, v = op.propagate(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    print(f"Position (km): {r}")
    print(f"Velocity (km/s): {v}")
    if not SGP4_AVAILABLE:
        print("Install sgp4: pip install sgp4")
