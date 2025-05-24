"use strict";
var cwmap = (() => {
  let protocol = new pmtiles.Protocol();
  maplibregl.addProtocol("pmtiles", protocol.tile);

  protocol.add(p);

  const map = new maplibregl.Map({
      container: "#map",
      zoom: h.maxZoom - 8,
      center: [h.centerLon, h.centerLat],
      style:
        "https://api.protomaps.com/styles/v5/light/en.json?key=dce60796ad799401",
    });
});
