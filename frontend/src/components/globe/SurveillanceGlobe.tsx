import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { SpatialCluster } from '../../types';

interface SurveillanceGlobeProps {
  isolates: SpatialCluster[];
  onSelectIsolate?: (isolate: SpatialCluster) => void;
}

export const SurveillanceGlobe: React.FC<SurveillanceGlobeProps> = ({ isolates, onSelectIsolate }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [hoveredIsolate, setHoveredIsolate] = useState<SpatialCluster | null>(null);

  useEffect(() => {
    if (!mountRef.current) return;
    const container = mountRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.z = 240;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // 2. Base Earth Sphere
    const globeRadius = 80;
    const sphereGeometry = new THREE.SphereGeometry(globeRadius, 64, 64);
    const sphereMaterial = new THREE.MeshPhongMaterial({
      color: 0x0f172a, // Slate 900
      emissive: 0x050a14,
      specular: 0x1e293b,
      shininess: 15,
      transparent: true,
      opacity: 0.95,
    });
    const globeMesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
    scene.add(globeMesh);

    // 3. Grid & Latitude/Longitude Wireframe
    const wireframeGeo = new THREE.WireframeGeometry(new THREE.SphereGeometry(globeRadius * 1.002, 32, 16));
    const wireframeMat = new THREE.LineBasicMaterial({
      color: 0x1e293b,
      transparent: true,
      opacity: 0.4,
    });
    const wireframe = new THREE.LineSegments(wireframeGeo, wireframeMat);
    scene.add(wireframe);

    // 4. Atmospheric Halo
    const haloGeo = new THREE.SphereGeometry(globeRadius * 1.15, 32, 32);
    const haloMat = new THREE.ShaderMaterial({
      vertexShader: `
        varying vec3 vNormal;
        void main() {
          vNormal = normalize(normalMatrix * normal);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vNormal;
        void main() {
          float intensity = pow(0.6 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 2.0);
          gl_FragColor = vec4(0.8, 0.1, 0.1, 1.0) * intensity * 0.35;
        }
      `,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      transparent: true,
    });
    const halo = new THREE.Mesh(haloGeo, haloMat);
    scene.add(halo);

    // 5. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);
    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(150, 150, 150);
    scene.add(dirLight);

    // 6. Map Lat/Lon to 3D Coordinates
    const markerGroup = new THREE.Group();
    const markers: { mesh: THREE.Mesh; isolate: SpatialCluster }[] = [];

    const latLonToVector3 = (lat: number, lon: number, radius: number) => {
      const phi = (90 - lat) * (Math.PI / 180);
      const theta = (lon + 180) * (Math.PI / 180);
      return new THREE.Vector3(
        -radius * Math.sin(phi) * Math.cos(theta),
        radius * Math.cos(phi),
        radius * Math.sin(phi) * Math.sin(theta)
      );
    };

    isolates.forEach((iso) => {
      const pos = latLonToVector3(iso.latitude, iso.longitude, globeRadius * 1.015);
      const hasCarb = iso.carbapenemases && iso.carbapenemases.length > 0;
      const hasCol = iso.colistin_genes && iso.colistin_genes.length > 0;

      // Color scheme: Carbapenemase (Crimson), Colistin (Purple), Susceptible (Emerald)
      const color = hasCol ? 0x9333ea : (hasCarb ? 0xdc2626 : 0x059669);
      const markerGeo = new THREE.SphereGeometry(1.8, 16, 16);
      const markerMat = new THREE.MeshBasicMaterial({ color });
      const marker = new THREE.Mesh(markerGeo, markerMat);
      marker.position.copy(pos);
      markerGroup.add(marker);
      markers.push({ mesh: marker, isolate: iso });

      // Outward Beacon Spike
      const spikeEnd = pos.clone().multiplyScalar(1.08);
      const spikeGeo = new THREE.BufferGeometry().setFromPoints([pos, spikeEnd]);
      const spikeMat = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.7 });
      const spike = new THREE.Line(spikeGeo, spikeMat);
      markerGroup.add(spike);
    });

    scene.add(markerGroup);

    // 7. Mouse Drag Interaction & Raycasting
    let isDragging = false;
    let prevMousePosition = { x: 0, y: 0 };

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        const deltaX = e.clientX - prevMousePosition.x;
        const deltaY = e.clientY - prevMousePosition.y;
        globeMesh.rotation.y += deltaX * 0.005;
        wireframe.rotation.y += deltaX * 0.005;
        markerGroup.rotation.y += deltaX * 0.005;

        globeMesh.rotation.x += deltaY * 0.005;
        wireframe.rotation.x += deltaY * 0.005;
        markerGroup.rotation.x += deltaY * 0.005;

        prevMousePosition = { x: e.clientX, y: e.clientY };
      } else {
        // Raycasting for isolate tooltip
        const rect = container.getBoundingClientRect();
        const mouse = new THREE.Vector2(
          ((e.clientX - rect.left) / width) * 2 - 1,
          -((e.clientY - rect.top) / height) * 2 + 1
        );
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(markers.map((m) => m.mesh));
        if (intersects.length > 0) {
          const hit = markers.find((m) => m.mesh === intersects[0].object);
          if (hit) setHoveredIsolate(hit.isolate);
        } else {
          setHoveredIsolate(null);
        }
      }
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    container.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // 8. Animation Loop (Continuous subtle idle rotation)
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (!isDragging) {
        globeMesh.rotation.y += 0.0015;
        wireframe.rotation.y += 0.0015;
        markerGroup.rotation.y += 0.0015;
      }
      renderer.render(scene, camera);
    };
    animate();

    // 9. Resize handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      container.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('resize', handleResize);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [isolates]);

  return (
    <div className="relative w-full h-full min-h-[460px] bg-slate-950/70 rounded-xl border border-slate-800 overflow-hidden">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* 3D Globe Legend Overlay */}
      <div className="absolute top-4 left-4 bg-slate-900/80 backdrop-blur-md border border-slate-700/60 p-3 rounded-lg text-xs space-y-2 pointer-events-none">
        <div className="font-semibold text-slate-200">Global Pathogen Distribution</div>
        <div className="flex items-center space-x-2 text-[11px]">
          <span className="w-2.5 h-2.5 rounded-full bg-crimson-600 inline-block"></span>
          <span className="text-slate-300">Carbapenemase-Producing (CRKP)</span>
        </div>
        <div className="flex items-center space-x-2 text-[11px]">
          <span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block"></span>
          <span className="text-slate-300">Colistin-Resistant (mcr / mgrB)</span>
        </div>
        <div className="flex items-center space-x-2 text-[11px]">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
          <span className="text-slate-300">Wild-Type / Susceptible</span>
        </div>
      </div>

      {/* Hovered Isolate Tooltip */}
      {hoveredIsolate && (
        <div className="absolute bottom-4 right-4 bg-slate-900/95 backdrop-blur-md border border-crimson-700/60 p-3.5 rounded-lg shadow-xl text-xs max-w-xs space-y-1 font-mono pointer-events-none">
          <div className="font-bold text-white text-sm flex justify-between">
            <span>{hoveredIsolate.accession}</span>
            <span className="text-emerald-400">{hoveredIsolate.sequence_type || 'ST?'}</span>
          </div>
          <div className="text-slate-400 text-[11px]">
            {hoveredIsolate.city}, {hoveredIsolate.country} ({hoveredIsolate.collection_year || 'N/A'})
          </div>
          <div className="pt-1 text-[11px]">
            <span className="text-slate-400">AMR Cargo: </span>
            <span className="text-crimson-400 font-semibold">
              {hoveredIsolate.carbapenemases.length > 0 ? hoveredIsolate.carbapenemases.join(', ') : 'None detected'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

