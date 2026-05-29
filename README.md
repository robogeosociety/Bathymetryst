# Bathymetryst

**Explore ancient shorelines.** Bathymetryst models how Earth's coastlines have
shifted between the last glacial maximum and today, and renders the change as an
interactive map you can scrub through with a slider.

When the great ice sheets grew (a **glacial maximum**), enormous volumes of water
were locked up as ice and global sea level fell by ~120 m — exposing continental
shelves and joining landmasses (Doggerland, Beringia, Sundaland). When the ice
melted (a **glacial minimum**, like today's interglacial), the seas rose and drowned
that land again. Bathymetryst lets you slide between those two worlds and see how
much land was gained or lost.

## The three goals

1. **Basemap** — the present-day coastline with major coastal cities, so changes are
   legible against a familiar world.
2. **DEM + data model** — a dynamic digital elevation model (DEM) of today's
   shorelines, plus a data model that accommodates *historical* shoreline
   reconstruction driven by past-climate (sea-level) data.
3. **GitHub Pages app** — a static site with a slider over the basemap that sweeps
   from glacial **maximum** (lowest sea level, most land) to glacial **minimum**
   (highest sea level, least land), redrawing the global shoreline and reporting the
   land gained or lost.

## How it works

Bathymetryst uses a **"bathtub" flood model** for its MVP: take a present-day
topo-bathy DEM (GEBCO / ETOPO), apply a single global sea-level offset, and classify
every cell as land or water. Drive that offset with a **paleo sea-level curve**
(≈ 0 m today → ≈ −120 m at the Last Glacial Maximum, ~20–26 ka) and you get a
shoreline for any point in the timeline. It's transparent, reproducible, and cheap
enough to precompute many slices for a smooth slider.

The bathtub model deliberately ignores glacial isostatic rebound, sediment, and
tectonics. A documented future extension swaps in **precomputed paleo-DEMs** per time
slice for geophysical accuracy — the data model is built so this requires no schema
changes (see `docs/data-model.md`).

## Tech stack

| Layer | Choice |
|-------|--------|
| Data pipeline | Python (`numpy`, `rasterio`/`rioxarray`, `geopandas`) |
| DEM source | GEBCO 2024 grid or NOAA ETOPO 2022 |
| Basemap data | Natural Earth coastlines + populated places |
| Web map | **MapLibre GL JS** (no API key) |
| Hosting | **GitHub Pages** via GitHub Actions |

## Repository layout

```
docs/        architecture, data model, and data-source specs
data/         sea-level curve, JSON Schemas (raw/ & processed/ are gitignored)
pipeline/     Python: fetch → model → manifest
web/          MapLibre GL JS GitHub Pages site (slider + stats)
.github/      Pages deploy workflow
```

## Quickstart

```bash
make setup     # create venv + install requirements
make data      # fetch DEM/basemap, run the model, build web/data/manifest.json
make serve     # serve web/ locally at http://localhost:8000
```

The web app ships with seed data, so `make serve` works before the full pipeline runs.
The pipeline's `fetch`/`model` steps are runnable stubs with `TODO`s — see
`CLAUDE.md` and `docs/architecture.md` for what to implement next.

## Deploying to GitHub Pages

Push to the default branch, then enable **Settings → Pages → Source: GitHub Actions**
(one-time, manual). The workflow in `.github/workflows/deploy-pages.yml` publishes the
`web/` directory.

## Data sources & credits

See `docs/data-sources.md`. Bathymetry/topography from **GEBCO** / **NOAA ETOPO**;
vectors from **Natural Earth**; sea-level curve seeded from **Spratt & Lisiecki
(2016)** and **Lambeck et al. (2014)**. Respect each source's license; large data
files are not committed.

## License

Apache License 2.0 — see `LICENSE`.
