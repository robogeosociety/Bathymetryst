// map.js — initialize MapLibre, add the present-day basemap and coastal cities.
// Exposes window.Bathymetryst.map (the map) and a ready promise for slider.js.

(function () {
  const map = new maplibregl.Map({
    container: "map",
    style: "https://demotiles.maplibre.org/style.json", // open vector basemap, no key
    center: [10, 30],
    zoom: 1.6,
    attributionControl: true,
  });
  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");

  // Resolve once style + sources are ready and basemap layers are added.
  const ready = new Promise((resolve) => {
    map.on("load", async () => {
      await addCities(map);
      await addCoastline(map);
      resolve(map);
    });
  });

  async function addCities(map) {
    let geojson;
    try {
      geojson = await fetch("data/cities.geojson").then((r) => r.json());
    } catch (e) {
      console.warn("cities.geojson not found; skipping city markers", e);
      return;
    }
    map.addSource("cities", { type: "geojson", data: geojson });
    map.addLayer({
      id: "city-dots",
      type: "circle",
      source: "cities",
      paint: {
        "circle-radius": [
          "interpolate", ["linear"], ["get", "population"],
          1000000, 3, 20000000, 9,
        ],
        "circle-color": "#ff6b6b",
        "circle-stroke-color": "#fff",
        "circle-stroke-width": 1,
      },
    });
    map.addLayer({
      id: "city-labels",
      type: "symbol",
      source: "cities",
      minzoom: 2.5,
      layout: { "text-field": ["get", "name"], "text-size": 11, "text-offset": [0, 1.1] },
      paint: { "text-color": "#fff", "text-halo-color": "#0b1f2a", "text-halo-width": 1.2 },
    });

    map.on("click", "city-dots", (e) => {
      const p = e.features[0].properties;
      new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(`<strong>${p.name}</strong><br/>${p.country}<br/>pop. ${Number(p.population).toLocaleString()}`)
        .addTo(map);
    });
    map.on("mouseenter", "city-dots", () => (map.getCanvas().style.cursor = "pointer"));
    map.on("mouseleave", "city-dots", () => (map.getCanvas().style.cursor = ""));
  }

  async function addCoastline(map) {
    // Present-day coastline overlay, if fetch_basemap.py has produced it.
    try {
      const data = await fetch("data/coastline.geojson").then((r) => {
        if (!r.ok) throw new Error("no coastline");
        return r.json();
      });
      map.addSource("coastline", { type: "geojson", data });
      map.addLayer({
        id: "coastline-line",
        type: "line",
        source: "coastline",
        paint: { "line-color": "#46c2c8", "line-width": 0.8 },
      });
    } catch (_) {
      /* optional; present basemap already shows today's coast */
    }
  }

  window.Bathymetryst = window.Bathymetryst || {};
  window.Bathymetryst.map = map;
  window.Bathymetryst.ready = ready;
})();
