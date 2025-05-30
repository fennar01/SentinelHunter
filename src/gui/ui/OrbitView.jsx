// OrbitView.jsx
// CesiumJS 3-D track visualiser
// SentinelHunter GUI

/**
 * OrbitView visualises satellite orbits in 3D using CesiumJS.
 * This minimal demo renders a Cesium globe and a hardcoded satellite path.
 */
import React, { useEffect, useRef } from 'react';

export default function OrbitView() {
  const cesiumContainer = useRef(null);

  useEffect(() => {
    // Dynamically import Cesium to avoid SSR issues
    import('cesium/Cesium').then(Cesium => {
      // Minimal CesiumJS setup
      if (!cesiumContainer.current) return;
      const viewer = new Cesium.Viewer(cesiumContainer.current, {
        timeline: false,
        animation: false,
      });
      // Add a hardcoded satellite track (polyline)
      viewer.entities.add({
        name: 'Demo Satellite Track',
        polyline: {
          positions: Cesium.Cartesian3.fromDegreesArray([0, 0, 10, 10, 20, 20, 30, 30]),
          width: 3,
          material: Cesium.Color.RED,
        },
      });
      viewer.zoomTo(viewer.entities);
      return () => viewer.destroy();
    });
  }, []);

  return (
    <div>
      <h2>OrbitView CesiumJS Demo</h2>
      <div ref={cesiumContainer} style={{ width: '600px', height: '400px' }} />
    </div>
  );
}
