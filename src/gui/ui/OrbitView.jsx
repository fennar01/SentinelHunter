// OrbitView.jsx
// CesiumJS 3-D track visualiser
// SentinelHunter GUI

/**
 * OrbitView visualises satellite orbits in 3D using CesiumJS.
 * Loads demo satellite data from a JSON file and plots tracks.
 */
import React, { useEffect, useRef } from 'react';

export default function OrbitView() {
  const cesiumContainer = useRef(null);

  useEffect(() => {
    async function loadAndPlot() {
      // Load demo satellite data
      const resp = await fetch('/src/gui/data/demo_satellites.json');
      const sats = await resp.json();
      const Cesium = await import('cesium/Cesium');
      if (!cesiumContainer.current) return;
      const viewer = new Cesium.Viewer(cesiumContainer.current, {
        timeline: false,
        animation: false,
      });
      sats.forEach(sat => {
        viewer.entities.add({
          name: sat.name,
          polyline: {
            positions: Cesium.Cartesian3.fromDegreesArrayHeights(sat.track.flat()),
            width: 3,
            material: Cesium.Color.YELLOW,
          },
        });
      });
      viewer.zoomTo(viewer.entities);
      return () => viewer.destroy();
    }
    loadAndPlot();
  }, []);

  return (
    <div>
      <h2>OrbitView CesiumJS Demo</h2>
      <div ref={cesiumContainer} style={{ width: '600px', height: '400px' }} />
    </div>
  );
}
