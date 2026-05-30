# data/

- **`sea_level_curve.csv`** — committed. Paleo sea-level control points (year-BP →
  global sea level in metres). Approximate/illustrative seed values; see
  `../docs/data-sources.md`.
- **`schema/`** — committed. JSON Schemas that are the source of truth for the data
  model (mirrored by `../pipeline/models.py`).
- **`raw/`** — gitignored. Downloaded DEM and Natural Earth files land here.
- **`processed/`** — gitignored. Per-slice masks / overlays produced by the model.

Run `make data` to populate `raw/` and `processed/` and (re)build
`../web/data/manifest.json`.
