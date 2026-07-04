"""Assemble web/data/manifest.json -- the single contract the web app reads.

Stdlib-only and runnable today:

    python -m pipeline.build_manifest

It joins each configured sea-level slice (config.SEA_LEVEL_SLICES_M) to a year-BP
via the sea-level curve and emits a flattened TimeSlice + ShorelineLayer per slice.

Until model_shoreline.py is implemented, land areas are ILLUSTRATIVE estimates of
continental-shelf exposure (see ESTIMATED_DELTA_KM2). Once real ShorelineLayers
exist, pass them to build_manifest(layers=...) to use measured areas instead.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
from typing import Optional

from . import config
from .fetch_dem import dem_metadata
from .models import Manifest
from .sea_level import load_curve, years_at

# Illustrative cumulative land *gained* (km^2) relative to present at each offset.
# Placeholder shelf-exposure estimates; replaced by measured areas once the model runs.
ESTIMATED_DELTA_KM2 = {
    0.0: 0.0,
    -20.0: 6_000_000.0,
    -40.0: 10_500_000.0,
    -60.0: 14_000_000.0,
    -80.0: 16_800_000.0,
    -100.0: 19_000_000.0,
    -120.0: 20_500_000.0,
}


def _label_for(level_m: float, years_bp: float) -> str:
    if level_m == 0.0:
        return "Present (glacial minimum)"
    if level_m <= -120.0:
        return f"Last Glacial Maximum (~{round(years_bp / 1000)} ka)"
    return f"{abs(level_m):.0f} m below present (~{round(years_bp / 1000)} ka)"


def build_manifest(layers: Optional[list] = None) -> Manifest:
    """Build a Manifest. If `layers` (ShorelineLayer list) is given, use its areas."""
    curve = load_curve()
    measured = {round(layer.sea_level_m, 3): layer for layer in (layers or [])}

    slices = []
    for level in config.SEA_LEVEL_SLICES_M:
        years_bp = years_at(level, curve)
        layer = measured.get(round(level, 3))
        if layer is not None:
            land_area = layer.land_area_km2
            delta = layer.land_delta_km2
            overlay = layer.overlay_url
        else:
            delta = ESTIMATED_DELTA_KM2.get(level, 0.0)
            land_area = config.PRESENT_LAND_AREA_KM2 + delta
            overlay = None
        slices.append(
            {
                "id": f"t{int(abs(level))}",
                "label": _label_for(level, years_bp),
                "years_before_present": years_bp,
                "sea_level_m": level,
                "source_method": config.SOURCE_METHOD,
                "overlay_url": overlay,
                "land_area_km2": land_area,
                "land_delta_km2": delta,
            }
        )

    slices.sort(key=lambda s: s["sea_level_m"])  # ascending: -120 .. 0
    return Manifest(
        generated_at=_dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        present_land_area_km2=config.PRESENT_LAND_AREA_KM2,
        slices=slices,
        dem=dem_metadata().to_dict(),
    )


def write_manifest(path: str = None, layers: Optional[list] = None) -> str:
    path = path or config.MANIFEST_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    manifest = build_manifest(layers=layers)
    with open(path, "w") as fh:
        json.dump(manifest.to_dict(), fh, indent=2)
    return path


if __name__ == "__main__":
    out = write_manifest()
    print(f"Wrote {out}")
