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
    center: [-122.6765, 45.4831], // Default Portland coordinates
    zoom: 9
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
        'circle-radius': 8,
        'circle-color': '#007bff',
        'circle-stroke-width': 2,
        'circle-stroke-color': '#ffffff',
        'circle-opacity': 0.8,
        'circle-pitch-alignment': 'viewport',  // Better for click detection
        'circle-translate-anchor': 'map'       // Ensure proper positioning
      }
    });
    
    // Add interactivity
    map.on('click', 'schools', (e) => {
        // Add radius and check both viewport and map-aligned features
        const features = map.queryRenderedFeatures(e.point, {
            layers: ['schools'],
            radius: 10,  // 10 pixel detection radius
            includeImages: true
        });
        
        if (!features.length) return;
        
        const feature = features[0];
        // Use coordinates from the actual click event instead of feature geometry
        new maplibregl.Popup()
            .setLngLat(e.lngLat)  // Use click coordinates instead of feature coordinates
            .setHTML(`
                <h3><a href="${feature.properties.website}" target="_blank">${feature.properties.name}</a></h3>
                <p>${feature.properties.address}</p>
                <p>${feature.properties.description}</p>
            `)
            .addTo(map);
    });

    // Change cursor style on hover
    map.on('mouseenter', 'schools', () => {
        map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'schools', () => {
        map.getCanvas().style.cursor = '';
    });
  });
})();
