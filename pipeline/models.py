"""Data model for Bathymetryst.

Dataclasses mirroring data/schema/*.json. Keep these in sync with the schemas;
see docs/data-model.md. Stdlib-only so this imports without the geo dependencies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class TimeSlice:
    """A point on the climate-driven timeline."""

    id: str
    label: str
    years_before_present: float
    global_sea_level_m: float
    source: str
    ice_volume_proxy: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "TimeSlice":
        return cls(**d)


@dataclass
class ShorelineLayer:
    """Renderable shoreline result for a time slice. Method-agnostic."""

    time_slice_id: str
    sea_level_m: float
    source_method: str  # "bathtub" | "paleodem"
    land_area_km2: float
    land_delta_km2: float
    overlay_url: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ShorelineLayer":
        return cls(**d)


@dataclass
class City:
    """A major coastal city for the present-day basemap."""

    name: str
    country: str
    lat: float
    lon: float
    population: int
    elevation_m: Optional[float] = None
    submerged_below_sea_level_m: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "City":
        return cls(**d)


@dataclass
class DEMMetadata:
    """Provenance for the elevation grid the model runs on."""

    source: str
    resolution_arcsec: float
    bounds: list  # [west, south, east, north]
    crs: str
    vertical_datum: str
    retrieved_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "DEMMetadata":
        return cls(**d)


@dataclass
class Manifest:
    """The single file the web app reads (web/data/manifest.json)."""

    generated_at: str
    present_land_area_km2: float
    slices: list = field(
        default_factory=list
    )  # flattened TimeSlice + ShorelineLayer dicts
    dem: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)
