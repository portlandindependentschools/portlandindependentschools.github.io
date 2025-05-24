"use strict";
var cwmap = (() => {
  let protocol = new pmtiles.Protocol();
  maplibregl.addProtocol("pmtiles", protocol.tile);
  
  // Initialize PMTiles source
  const p = new pmtiles.PMTiles("your_school_data.pmtiles"); // Update with your PMTiles URL
  protocol.add(p);

  const map = new maplibregl.Map({
    container: "map",
    style: "https://api.protomaps.com/styles/v5/light/en.json?key=dce60796ad799401",
    center: [-122.6765, 45.5231], // Default Portland coordinates
    zoom: 10
  });

  // Add school markers after map loads
  map.on('load', () => {
    // Add your school data source
    map.addSource('schools', {
      type: 'geojson',
      data: schoolsData  // Now using the properly formatted GeoJSON
    });

    // Add marker layer
    map.addLayer({
      id: 'schools',
      type: 'circle',
      source: 'schools',
      paint: {
        'circle-radius': 6,
        'circle-color': '#007bff',
        'circle-stroke-width': 1,
        'circle-stroke-color': '#fff'
      }
    });
  });
})();
