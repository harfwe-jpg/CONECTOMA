/**
 * TRACTOGRAFÍA AXONAL Y SIMULACIÓN DE POTENCIALES DE ACCIÓN (Three.js)
 * Modela haces de fibras de sustancia blanca como curvas 3D (Splines)
 * y emite pulsos de fotones que representan potenciales de acción propagándose.
 */

class TractographySystem {
  constructor(scene) {
    this.scene = scene;
    this.tracts = [];
    this.tractLinesGroup = new THREE.Group();
    this.particlesGroup = new THREE.Group();
    this.scene.add(this.tractLinesGroup);
    this.scene.add(this.particlesGroup);

    // Pool de pulsos de potenciales de acción
    this.pulses = [];
    this.maxPulses = 220;
    this.initPulsePool();
  }

  initPulsePool() {
    // Geometría y material compartido para máximo rendimiento WebGL
    const geom = new THREE.SphereGeometry(0.35, 8, 8);
    const mat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending
    });

    for (let i = 0; i < this.maxPulses; i++) {
      const mesh = new THREE.Mesh(geom, mat.clone());
      mesh.visible = false;
      this.particlesGroup.add(mesh);
      this.pulses.push({
        mesh: mesh,
        active: false,
        curve: null,
        progress: 0.0,
        speed: 0.005,
        color: 0x00f0ff
      });
    }
  }

  buildTracts(tractsData, nodesMap) {
    // Limpiar geometrías previas si existieran
    while (this.tractLinesGroup.children.length > 0) {
      const obj = this.tractLinesGroup.children[0];
      this.tractLinesGroup.remove(obj);
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    }

    this.tracts = [];

    tractsData.forEach((tData, idx) => {
      const srcNode = nodesMap[tData.src];
      const tgtNode = nodesMap[tData.tgt];
      if (!srcNode || !tgtNode) return;

      const p1 = new THREE.Vector3(...srcNode.pos);
      const p2 = new THREE.Vector3(...tgtNode.pos);

      // Calcular punto de control intermedio para curvatura orgánica natural
      const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
      
      // Si conecta a través de hemisferios o lóbulo superior, arquear hacia arriba/centro
      const dist = p1.distanceTo(p2);
      if (tData.type === "CorpusCallosum") {
        mid.z += 8.0; // Arco comisural del cuerpo calloso
      } else if (tData.type === "Reward" || tData.type === "Sexual") {
        mid.z += 2.5; // Haz prosencefálico medial
      } else {
        mid.y += (mid.y > 0 ? 3.0 : -3.0);
      }

      const curve = new THREE.CatmullRomCurve3([p1, mid, p2]);
      const points = curve.getPoints(24);
      const lineGeom = new THREE.BufferGeometry().setFromPoints(points);

      // Material sutil con transparencia aditiva
      const lineMat = new THREE.LineBasicMaterial({
        color: 0x1e293b,
        transparent: true,
        opacity: 0.22,
        blending: THREE.AdditiveBlending
      });

      const line = new THREE.Line(lineGeom, lineMat);
      line.userData = {
        tractIndex: idx,
        src: tData.src,
        tgt: tData.tgt,
        type: tData.type,
        baseColor: 0x1e293b,
        curve: curve,
        activity: 0.0
      };

      this.tractLinesGroup.add(line);
      this.tracts.push(line);
    });
  }

  updateActivations(activeTractsList, primaryColorHex = 0x00f0ff) {
    const activeMap = {};
    activeTractsList.forEach(item => {
      activeMap[item.index] = item.activity;
    });

    this.tracts.forEach(line => {
      const idx = line.userData.tractIndex;
      const activity = activeMap[idx] || 0.0;
      line.userData.activity = activity;

      if (activity > 0.1) {
        // Iluminar la fibra en proporción a la actividad sináptica
        line.material.color.setHex(primaryColorHex);
        line.material.opacity = 0.35 + activity * 0.55;

        // Ocasionalmente disparar un pulso (potencial de acción)
        if (Math.random() < 0.25 * activity) {
          this.spawnPulse(line.userData.curve, primaryColorHex, 0.008 + activity * 0.015);
        }
      } else {
        // Fibra en reposo basal
        line.material.color.setHex(0x1e293b);
        line.material.opacity = 0.15;
      }
    });
  }

  spawnPulse(curve, colorHex, speed) {
    // Buscar pulso inactivo en el pool
    const pulse = this.pulses.find(p => !p.active);
    if (!pulse) return;

    pulse.active = true;
    pulse.curve = curve;
    pulse.progress = 0.0;
    pulse.speed = speed;
    pulse.mesh.material.color.setHex(colorHex);
    pulse.mesh.visible = true;
    
    // Posición inicial
    const startPt = curve.getPointAt(0);
    pulse.mesh.position.copy(startPt);
  }

  animate() {
    // Mover los pulsos activos a lo largo de las curvas axónicas
    for (let i = 0; i < this.pulses.length; i++) {
      const p = this.pulses[i];
      if (!p.active) continue;

      p.progress += p.speed;
      if (p.progress >= 1.0) {
        // El potencial de acción alcanzó el terminal sináptico
        p.active = false;
        p.mesh.visible = false;
        continue;
      }

      const currentPos = p.curve.getPointAt(p.progress);
      p.mesh.position.copy(currentPos);
      
      // Pulso brillante que crece y decrece
      const scale = Math.sin(p.progress * Math.PI) * 1.5 + 0.6;
      p.mesh.scale.set(scale, scale, scale);
    }
  }

  setTractsVisibility(visible) {
    this.tractLinesGroup.visible = visible;
    this.particlesGroup.visible = visible;
  }
}

window.TractographySystem = TractographySystem;
