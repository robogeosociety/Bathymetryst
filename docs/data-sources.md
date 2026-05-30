# Data sources

Large source files are **not committed** (see `.gitignore`). Fetch them via the
pipeline and respect each provider's license/attribution.

## Elevation (DEM) — topography + bathymetry

| Source | Description | Link |
|--------|-------------|------|
| **GEBCO 2024 Grid** | Global ~15 arc-second topo-bathy grid (continuous land+ocean) | https://www.gebco.net/data_and_products/gridded_bathymetry_data/ |
| **NOAA ETOPO 2022** | Global relief, bedrock & ice-surface variants, 15/30/60 arc-sec | https://www.ncei.noaa.gov/products/etopo-global-relief-model |

Either works for the bathtub model; both are continuous land+sea elevation grids in
EPSG:4326. Record which one in `DEMMetadata`. GEBCO is the default in `config.py`.

## Vectors — coastline & cities

| Source | Layer | Link |
|--------|-------|------|
| **Natural Earth** | `ne_10m_coastline` (present coastline) | https://www.naturalearthdata.com/ |
| **Natural Earth** | `ne_10m_populated_places` (cities + population) | https://www.naturalearthdata.com/ |

Public domain. `fetch_basemap.py` filters populated places to major coastal cities and
writes `web/data/cities.geojson`.

## Paleo sea-level curve

`data/sea_level_curve.csv` seeds control points (year-BP → global sea level in metres)
from the literature. These are **approximate, illustrative** values for the MVP;
replace with digitized published series for rigor.

| Source | Coverage | Reference |
|--------|----------|-----------|
| **Lambeck et al. (2014)** | LGM → Holocene, ice-volume-equivalent sea level | *PNAS* 111(43):15296–15303 |
| **Spratt & Lisiecki (2016)** | 0–800 ka sea-level stack | *Climate of the Past* 12:1079–1092 |

Key anchors used: present ≈ 0 m; LGM lowstand ≈ −120 to −134 m at ~20–26 ka.

## Licensing summary

- **GEBCO** — free to use with attribution; review the GEBCO terms.
- **NOAA ETOPO** — U.S. Government work, public domain.
- **Natural Earth** — public domain.
- **Sea-level papers** — cite the authors; do not redistribute paywalled figures.
