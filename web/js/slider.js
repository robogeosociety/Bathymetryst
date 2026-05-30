// slider.js — load the manifest, wire the slider to slices, swap shoreline overlays.

(function () {
  const B = (window.Bathymetryst = window.Bathymetryst || {});
  const slider = document.getElementById("slider");
  const OVERLAY_LAYER = "shoreline-overlay";
  const OVERLAY_SOURCE = "shoreline-overlay-src";

  let slices = []; // ordered by sea_level_m descending: 0 (today) -> -120 (LGM)

  async function init() {
    const map = await B.ready;
    const manifest = await fetch("data/manifest.json").then((r) => r.json());

    // Slider left = glacial minimum (today, highest sea level); right = glacial maximum.
    slices = manifest.slices.slice().sort((a, b) => b.sea_level_m - a.sea_level_m);
    slider.max = String(slices.length - 1);
    slider.value = "0";

    slider.addEventListener("input", () => select(map, Number(slider.value)));
    select(map, 0);
  }

  function select(map, index) {
    const slice = slices[index];
    if (!slice) return;
    B.renderStats(slice);
    swapOverlay(map, slice);
  }

  function swapOverlay(map, slice) {
    // Remove any previous overlay.
    if (map.getLayer(OVERLAY_LAYER)) map.removeLayer(OVERLAY_LAYER);
    if (map.getSource(OVERLAY_SOURCE)) map.removeSource(OVERLAY_SOURCE);
    if (!slice.overlay_url) return; // seed data has no overlay yet

    const url = slice.overlay_url;
    if (url.endsWith(".geojson") || url.endsWith(".json")) {
      map.addSource(OVERLAY_SOURCE, { type: "geojson", data: url });
      map.addLayer({
        id: OVERLAY_LAYER,
        type: "fill",
        source: OVERLAY_SOURCE,
        paint: { "fill-color": "#f2c14e", "fill-opacity": 0.45 },
      });
    } else {
      // Raster overlay (PNG/tiles) covering the configured bounds.
      map.addSource(OVERLAY_SOURCE, {
        type: "image",
        url: url,
        coordinates: [[-180, 90], [180, 90], [180, -90], [-180, -90]],
      });
      map.addLayer({
        id: OVERLAY_LAYER,
        type: "raster",
        source: OVERLAY_SOURCE,
        paint: { "raster-opacity": 0.6 },
      });
    }
  }

  init().catch((e) => console.error("Bathymetryst init failed", e));
})();
