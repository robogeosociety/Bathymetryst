# Architecture

Bathymetryst has two halves: a **Python data pipeline** that turns raw geodata into
web-ready slices, and a **static MapLibre web app** that renders them. They are
decoupled by a single contract file: `web/data/manifest.json`.

## Data flow

```
            ┌─────────────────┐      ┌────────────────────┐
 GEBCO/     │ fetch_dem.py    │      │ fetch_basemap.py   │   Natural Earth
 ETOPO  ───▶│ → data/raw/dem  │      │ → coastline+cities │◀── (coastline,
            └────────┬────────┘      └─────────┬──────────┘     populated_places)
                     │                         │
                     ▼                         ▼
            ┌─────────────────┐      web/data/cities.geojson
 sea_level  │ model_shoreline │      web/data/coastline.geojson
 curve  ───▶│ DEM + offset →  │
 (.csv)     │ land/water mask │
            │ + land_area_km2 │
            └────────┬────────┘
                     ▼
            data/processed/<slice>.{tif,geojson,png}   (gitignored)
                     │
                     ▼
            ┌─────────────────┐
            │ build_manifest  │ → web/data/manifest.json  (committed)
            └────────┬────────┘
                     ▼
            ┌─────────────────────────────────────────┐
            │ web/  (MapLibre GL JS, static)            │
            │  map.js   basemap + city markers          │
            │  slider.js  offset → active slice/overlay │
            │  stats.js   land gained/lost readout       │
            └─────────────────────────────────────────┘
```

## Components

### Pipeline (`pipeline/`)
- **`config.py`** — paths, DEM source URLs, the set of sea-level slices to generate
  (e.g. 0 to −120 m), and the map bounds/resolution. Single place to tune.
- **`models.py`** — dataclasses (`TimeSlice`, `ShorelineLayer`, `City`, `DEMMetadata`)
  mirroring `data/schema/*.json`. Provides `to_dict`/`from_dict` for JSON round-trips.
- **`sea_level.py`** — loads `data/sea_level_curve.csv` and linearly interpolates a
  global sea-level offset for any year-BP (stdlib only; runnable: `python -m pipeline.sea_level`).
- **`fetch_dem.py`** 🚧 — download & cache the global topo-bathy grid. Stub with TODO.
- **`fetch_basemap.py`** 🚧 — produce `coastline.geojson` + `cities.geojson` from
  Natural Earth. Stub with TODO.
- **`model_shoreline.py`** 🚧 — the bathtub model: `water = dem < offset`; emit a mask
  and land-area stats per slice. Stub with TODO.
- **`build_manifest.py`** — assemble `web/data/manifest.json` from the slice config and
  the sea-level curve (stdlib only; runnable today, fills real areas once the model runs).

### Web app (`web/`)
Static, no build step. MapLibre GL JS loaded from CDN. `map.js` initializes the map
with an open basemap and adds city markers; `slider.js` maps the slider position to the
nearest `TimeSlice` in the manifest and swaps/crossfades its shoreline overlay;
`stats.js` updates the land gained/lost panel. All three read only `web/data/*`.

## Why this split

- The web app must run on **GitHub Pages** (static hosting) with **no server**, so all
  heavy computation happens offline in the pipeline and is baked into committed
  artifacts + (large) generated overlays.
- Keeping the contract to one `manifest.json` means the modeling method can change
  (bathtub → paleo-DEM) without touching the front end.

## Future extensions
- Replace per-slice GeoJSON overlays with raster/vector **tiles** for performance at
  global zoom.
- Swap `source_method: "bathtub"` for `"paleodem"` slices that correct for glacial
  isostatic adjustment (GIA).
- Add named-feature callouts (Doggerland, Beringia, Sundaland) keyed to sea-level range.
