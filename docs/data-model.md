# Data model

The data model is the contract that lets a *historical* shoreline be described
independently of how it was computed. Schemas are the source of truth in
`data/schema/*.json`; `pipeline/models.py` mirrors them as Python dataclasses. Keep the
two in sync.

## Entities

### TimeSlice
A point on the climate-driven timeline — the axis the slider walks.

| field | type | notes |
|-------|------|-------|
| `id` | string | stable id, e.g. `"t0"`, `"lgm"` |
| `label` | string | human label, e.g. `"Last Glacial Maximum"` |
| `years_before_present` | number | BP = before 1950 CE |
| `global_sea_level_m` | number | offset vs present datum; **negative below** |
| `ice_volume_proxy` | number? | optional (e.g. δ¹⁸O), for provenance |
| `source` | string | citation key, e.g. `"lambeck2014"` |

### ShorelineLayer
The renderable result for a slice. **Method-agnostic** so a future paleo-DEM source
slots in unchanged.

| field | type | notes |
|-------|------|-------|
| `time_slice_id` | string | FK → `TimeSlice.id` |
| `sea_level_m` | number | the offset applied |
| `source_method` | enum | `"bathtub"` \| `"paleodem"` |
| `overlay_url` | string? | relative URL to GeoJSON/PNG/tiles; `null` for seed |
| `land_area_km2` | number | total land at this sea level |
| `land_delta_km2` | number | land vs present (positive = land gained) |

### City
Major coastal city for the basemap.

| field | type | notes |
|-------|------|-------|
| `name` | string | |
| `country` | string | |
| `lat` / `lon` | number | EPSG:4326 |
| `population` | integer | |
| `elevation_m` | number? | present-day ground elevation |
| `submerged_below_sea_level_m` | number? | offset at which it floods (if ever) |

### DEMMetadata
Provenance for the elevation grid the model runs on.

| field | type | notes |
|-------|------|-------|
| `source` | string | `"GEBCO_2024"`, `"ETOPO_2022"`, … |
| `resolution_arcsec` | number | e.g. 15 |
| `bounds` | [w,s,e,n] | EPSG:4326 |
| `crs` | string | e.g. `"EPSG:4326"` |
| `vertical_datum` | string | e.g. `"MSL"` |
| `retrieved_at` | string | ISO 8601 |

## The manifest

`build_manifest.py` writes `web/data/manifest.json`, the single file the web app reads:

```json
{
  "generated_at": "2026-05-29T00:00:00Z",
  "dem": { "...": "DEMMetadata" },
  "present_land_area_km2": 148940000,
  "slices": [
    {
      "id": "t0",
      "label": "Present (glacial minimum)",
      "years_before_present": 0,
      "sea_level_m": 0.0,
      "source_method": "bathtub",
      "overlay_url": null,
      "land_area_km2": 148940000,
      "land_delta_km2": 0
    }
  ]
}
```

`slices` flattens a `TimeSlice` joined to its `ShorelineLayer`. Slices are ordered by
`sea_level_m` so the slider can index them directly.

## Modeling caveats (bathtub model)

The MVP floods a present-day DEM with a uniform global offset. It therefore **ignores**:
- **Glacial isostatic adjustment** — crust rebounds/depresses under ice load; real
  paleo-shorelines differ from a naive flood, especially near former ice sheets.
- **Hydrologic connectivity** — every cell below the offset is "water", including
  closed basins that wouldn't actually flood.
- **Sediment & tectonics** — shelf morphology has changed over 10⁴–10⁵ years.

These are acceptable for an illustrative global visualization. The `paleodem`
`source_method` exists to supersede them later without breaking the schema.
