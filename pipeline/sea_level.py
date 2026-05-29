"""Load and interpolate the paleo sea-level curve.

Stdlib-only and runnable directly:

    python -m pipeline.sea_level [years_before_present]

Provides linear interpolation in both directions:
  - level_at(years_bp)  -> global sea-level offset in metres
  - years_at(level_m)   -> nearest year-BP for a target sea level
"""

from __future__ import annotations

import csv
import sys
from bisect import bisect_left
from typing import List, Tuple

from . import config


def load_curve(path: str = None) -> List[Tuple[float, float]]:
    """Return [(years_before_present, sea_level_m), ...] sorted by year-BP."""
    path = path or config.SEA_LEVEL_CSV
    points: List[Tuple[float, float]] = []
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or row[0].lstrip().startswith("#"):
                continue
            if row[0].strip() == "years_before_present":  # header
                continue
            points.append((float(row[0]), float(row[1])))
    points.sort(key=lambda p: p[0])
    if not points:
        raise ValueError(f"No data points found in {path}")
    return points


def _interp(x: float, xs: List[float], ys: List[float]) -> float:
    """Linear interpolation with flat extrapolation outside the range."""
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    i = bisect_left(xs, x)
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = ys[i - 1], ys[i]
    t = (x - x0) / (x1 - x0)
    return y0 + t * (y1 - y0)


def level_at(years_bp: float, curve: List[Tuple[float, float]] = None) -> float:
    """Global sea-level offset (m) at a given year-BP."""
    curve = curve or load_curve()
    xs = [p[0] for p in curve]
    ys = [p[1] for p in curve]
    return _interp(years_bp, xs, ys)


def years_at(level_m: float, curve: List[Tuple[float, float]] = None) -> float:
    """Nearest year-BP whose sea level matches the target (m).

    The curve is monotonic enough for the MVP that a nearest-point search is fine.
    """
    curve = curve or load_curve()
    return min(curve, key=lambda p: abs(p[1] - level_m))[0]


def _main(argv: List[str]) -> int:
    curve = load_curve()
    if len(argv) > 1:
        yr = float(argv[1])
        print(f"{yr:.0f} yr BP -> {level_at(yr, curve):.1f} m")
        return 0
    print(f"Loaded {len(curve)} control points from {config.SEA_LEVEL_CSV}")
    for yr in (0, 10000, 18000, 20000, 26000):
        print(f"  {yr:>6} yr BP -> {level_at(yr, curve):7.1f} m")
    print(f"  -120 m  -> ~{years_at(-120.0, curve):.0f} yr BP")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
