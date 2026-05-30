"""Tunable configuration for the Bathymetryst pipeline.

Single place to adjust data sources, the set of sea-level slices, and map extent.
"""

from __future__ import annotations

import os

# --- Paths -----------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SCHEMA_DIR = os.path.join(DATA_DIR, "schema")
SEA_LEVEL_CSV = os.path.join(DATA_DIR, "sea_level_curve.csv")

WEB_DIR = os.path.join(ROOT, "web")
WEB_DATA_DIR = os.path.join(WEB_DIR, "data")
MANIFEST_PATH = os.path.join(WEB_DATA_DIR, "manifest.json")

# --- DEM source ------------------------------------------------------------
# Default to GEBCO; switch to ETOPO by editing these. See docs/data-sources.md.
DEM_SOURCE = "GEBCO_2024"
DEM_RESOLUTION_ARCSEC = 15.0
DEM_VERTICAL_DATUM = "MSL"
DEM_DOWNLOAD_URL = ""  # TODO: fill with the chosen GEBCO/ETOPO grid URL

# --- Geographic extent -----------------------------------------------------
# [west, south, east, north] in EPSG:4326. Global by default.
BOUNDS = [-180.0, -90.0, 180.0, 90.0]
CRS = "EPSG:4326"

# --- Sea-level slices to generate -----------------------------------------
# Glacial minimum (0 m, present) -> glacial maximum (-120 m, LGM-ish).
# build_manifest maps each offset to the nearest year-BP via the sea-level curve.
SEA_LEVEL_SLICES_M = [0.0, -20.0, -40.0, -60.0, -80.0, -100.0, -120.0]

# Present-day land area baseline (km^2); land_delta is computed against this.
PRESENT_LAND_AREA_KM2 = 148_940_000.0

# Shoreline modeling method for generated slices.
SOURCE_METHOD = "bathtub"  # or "paleodem" once available
