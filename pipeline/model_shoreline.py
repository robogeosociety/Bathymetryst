"""Bathtub shoreline model: present-day DEM + global sea-level offset -> land/water.

STUB: implement the raster classification and area computation. Requires the geo
deps in requirements.txt (numpy + rasterio/rioxarray). See docs/data-model.md for
the modeling caveats.

Core idea (MVP):
    is_water = dem_elevation < sea_level_offset_m
    land_area = sum(cell_area for cells where not is_water)
"""

from __future__ import annotations

from . import config
from .models import ShorelineLayer


def model_slice(dem_path: str, sea_level_m: float, time_slice_id: str) -> ShorelineLayer:
    """Classify the DEM at one sea-level offset and return a ShorelineLayer.

    TODO:
      - Read the DEM (config.DEM_SOURCE) with rasterio/rioxarray.
      - mask = dem < sea_level_m  (water); land = ~mask.
      - Compute land_area_km2 using latitude-aware cell areas (EPSG:4326).
      - land_delta_km2 = land_area_km2 - config.PRESENT_LAND_AREA_KM2.
      - Write an overlay (GeoJSON polygons or PNG) to data/processed/ and set
        overlay_url to its web-relative path.
    """
    raise NotImplementedError(
        "model_slice is a stub. Implement the bathtub classification. "
        "See docs/data-model.md."
    )


def model_all(dem_path: str) -> list:
    """Run model_slice for every offset in config.SEA_LEVEL_SLICES_M."""
    return [
        model_slice(dem_path, lvl, f"t{int(abs(lvl))}")
        for lvl in config.SEA_LEVEL_SLICES_M
    ]


if __name__ == "__main__":
    print("model_shoreline: stub. Implement model_slice() / model_all().")
