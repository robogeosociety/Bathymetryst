"""Fetch and cache the global topo-bathy DEM (GEBCO / ETOPO).

STUB: implement the download + caching. See docs/data-sources.md for URLs and
config.py for the chosen source. Requires the geo deps in requirements.txt.
"""

from __future__ import annotations

import os

from . import config
from .models import DEMMetadata


def fetch_dem(force: bool = False) -> str:
    """Download the configured DEM grid into data/raw/ and return its path.

    TODO:
      - Resolve config.DEM_DOWNLOAD_URL (GEBCO_2024 or ETOPO_2022).
      - Stream-download to data/raw/, skipping if present unless force=True.
      - Optionally clip to config.BOUNDS and resample to DEM_RESOLUTION_ARCSEC.
    """
    os.makedirs(config.RAW_DIR, exist_ok=True)
    raise NotImplementedError(
        "fetch_dem is a stub. Set config.DEM_DOWNLOAD_URL and implement the download. "
        "See docs/data-sources.md."
    )


def dem_metadata() -> DEMMetadata:
    """Describe the DEM the pipeline is configured to use (provenance for the manifest)."""
    return DEMMetadata(
        source=config.DEM_SOURCE,
        resolution_arcsec=config.DEM_RESOLUTION_ARCSEC,
        bounds=config.BOUNDS,
        crs=config.CRS,
        vertical_datum=config.DEM_VERTICAL_DATUM,
        retrieved_at=None,
    )


if __name__ == "__main__":
    print(dem_metadata().to_dict())
