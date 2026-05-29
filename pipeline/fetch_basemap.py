"""Build the present-day basemap vectors from Natural Earth.

STUB: implement coastline + coastal-city extraction. Writes GeoJSON the web app
reads directly. See docs/data-sources.md. Requires the geo deps in requirements.txt.

Outputs:
  web/data/coastline.geojson   (from ne_10m_coastline)
  web/data/cities.geojson      (filtered ne_10m_populated_places)
"""

from __future__ import annotations

import os

from . import config


def fetch_coastline() -> str:
    """Download ne_10m_coastline and write web/data/coastline.geojson.

    TODO: download/cache the Natural Earth coastline, reproject to EPSG:4326 if
    needed, and dump GeoJSON.
    """
    os.makedirs(config.WEB_DATA_DIR, exist_ok=True)
    raise NotImplementedError("fetch_coastline is a stub. See docs/data-sources.md.")


def fetch_cities(min_population: int = 1_000_000, max_elevation_m: float = 50.0) -> str:
    """Download ne_10m_populated_places, filter to major coastal cities, write GeoJSON.

    TODO:
      - Load populated places (name, country, population, lat/lon).
      - Keep large cities near the coast (sample DEM elevation <= max_elevation_m,
        or distance-to-coast threshold).
      - Emit features matching the City schema -> web/data/cities.geojson.
    """
    os.makedirs(config.WEB_DATA_DIR, exist_ok=True)
    raise NotImplementedError("fetch_cities is a stub. See docs/data-sources.md.")


if __name__ == "__main__":
    print("fetch_basemap: stub. Implement fetch_coastline() and fetch_cities().")
