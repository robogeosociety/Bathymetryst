// stats.js — render the readout panel for the active slice.

(function () {
  const els = {
    sliceLabel: document.getElementById("sliceLabel"),
    seaLevel: document.getElementById("seaLevel"),
    years: document.getElementById("years"),
    landDelta: document.getElementById("landDelta"),
    note: document.getElementById("overlayNote"),
  };

  function fmtKm2(v) {
    const sign = v > 0 ? "+" : v < 0 ? "−" : "";
    return sign + Math.abs(Math.round(v)).toLocaleString();
  }

  function render(slice) {
    if (!slice) return;
    els.sliceLabel.textContent = slice.label;
    els.seaLevel.textContent = `${slice.sea_level_m > 0 ? "+" : ""}${slice.sea_level_m} m`;
    els.years.textContent = `${(slice.years_before_present / 1000).toFixed(1)} ka`;
    els.landDelta.textContent = fmtKm2(slice.land_delta_km2);
    els.note.textContent = slice.overlay_url
      ? ""
      : "Shoreline overlay pending — run the pipeline (make data). Land figures are illustrative estimates.";
  }

  window.Bathymetryst = window.Bathymetryst || {};
  window.Bathymetryst.renderStats = render;
})();
