/**
 * ESCENA 3D PRINCIPAL DEL CONECTOMA CEREBRAL (Three.js)
 * Administra el renderizador WebGL, cámara, iluminación, mallas de núcleos anatómicos,
 * partículas corticales y detección de interacción por Raycaster.
 */

class ConnectomeScene {
  constructor(canvasElement, onNodeHover, onNodeClick) {
    this.canvas = canvasElement;
    this.onNodeHover = onNodeHover;
    this.onNodeClick = onNodeClick;

    this.nodesMap = {};
    this.nucleiMeshes = [];
    this.cortexPoints = null;
    this.cortexData = [];
    this.tractography = null;

    this.currentViewMode = "full";
    this.autoRotate = true;

    this.initThree();
    this.initLights();
    this.initRaycaster();
    this.initEvents();
  }

  initThree() {
    // 1. Escena con niebla sutil neuro-espacial
    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x06080d, 0.007);

    // 2. Cámara de perspectiva
    this.camera = new THREE.PerspectiveCamera(
      45,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    this.camera.position.set(50, 40, 75);

    // 3. Renderizador WebGL de alta precisión
    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: false,
      powerPreference: "high-performance"
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.25;

    // 4. OrbitControls con amortiguación inercial
    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.maxDistance = 220;
    this.controls.minDistance = 15;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.6;

    // Grupo contenedor del cerebro
    this.brainGroup = new THREE.Group();
    this.scene.add(this.brainGroup);

    // Sistema de tractografía axonal
    this.tractography = new TractographySystem(this.brainGroup);
  }

  initLights() {
    const ambient = new THREE.AmbientLight(0x38bdf8, 0.4);
    this.scene.add(ambient);

    // Luz nuclear central en el diencéfalo
    this.coreLight = new THREE.PointLight(0x00f0ff, 1.8, 120);
    this.coreLight.position.set(0, 0, 0);
    this.scene.add(this.coreLight);

    // Luces periféricas de contorno
    const lightA = new THREE.DirectionalLight(0xa855f7, 0.8);
    lightA.position.set(60, 50, 40);
    this.scene.add(lightA);

    const lightB = new THREE.DirectionalLight(0x3b82f6, 0.6);
    lightB.position.set(-60, -40, -30);
    this.scene.add(lightB);
  }

  initRaycaster() {
    this.raycaster = new THREE.Raycaster();
    this.raycaster.params.Points.threshold = 1.5;
    this.mouse = new THREE.Vector2(-999, -999);
    this.intersectedObject = null;
  }

  initEvents() {
    window.addEventListener("resize", () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });

    this.canvas.addEventListener("mousemove", (e) => {
      this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
      this.checkIntersection();
    });

    this.canvas.addEventListener("click", () => {
      if (this.intersectedObject && this.onNodeClick) {
        this.onNodeClick(this.intersectedObject.userData);
      }
    });

    // Desactivar rotación automática temporalmente al interactuar con el mouse
    this.canvas.addEventListener("mousedown", () => {
      this.controls.autoRotate = false;
    });
  }

  loadConnectome(connectomeData) {
    this.nodesMap = {};
    connectomeData.nodes.forEach(n => {
      this.nodesMap[n.id] = n;
    });

    // 1. Construir núcleos anatómicos subcorticales y clave
    const nucleiList = connectomeData.nodes.filter(n => !n.id.startsWith("CORTEX_"));
    this.buildNuclei(nucleiList);

    // 2. Construir manto cortical de neuronas
    const cortexList = connectomeData.nodes.filter(n => n.id.startsWith("CORTEX_"));
    this.buildCorticalMantle(cortexList);

    // 3. Construir tractografía axonal de sustancia blanca
    this.tractography.buildTracts(connectomeData.tracts, this.nodesMap);
  }

  buildNuclei(nucleiList) {
    // Limpiar si existen
    this.nucleiMeshes.forEach(m => this.brainGroup.remove(m));
    this.nucleiMeshes = [];

    const sphereGeom = new THREE.SphereGeometry(1, 24, 24);

    nucleiList.forEach(node => {
      const baseColor = new THREE.Color(node.color || "#00f0ff");
      
      // Material PBR con brillo interno emisivo
      const mat = new THREE.MeshStandardMaterial({
        color: baseColor,
        emissive: baseColor,
        emissiveIntensity: 0.45,
        roughness: 0.25,
        metalness: 0.65,
        transparent: true,
        opacity: 0.95
      });

      const mesh = new THREE.Mesh(sphereGeom, mat);
      mesh.position.set(...node.pos);
      const rad = node.radius || 2.0;
      mesh.scale.set(rad, rad, rad);

      mesh.userData = {
        ...node,
        baseRadius: rad,
        baseColor: baseColor,
        isNucleus: true
      };

      // Halo resplandeciente externo (halo sprite)
      const haloMat = new THREE.MeshBasicMaterial({
        color: baseColor,
        transparent: true,
        opacity: 0.2,
        blending: THREE.AdditiveBlending,
        wireframe: true
      });
      const halo = new THREE.Mesh(sphereGeom, haloMat);
      halo.scale.set(1.4, 1.4, 1.4);
      mesh.add(halo);

      this.brainGroup.add(mesh);
      this.nucleiMeshes.push(mesh);
    });
  }

  buildCorticalMantle(cortexList) {
    if (this.cortexPoints) {
      this.brainGroup.remove(this.cortexPoints);
      this.cortexPoints.geometry.dispose();
      this.cortexPoints.material.dispose();
    }

    this.cortexData = cortexList;
    const count = cortexList.length;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const sizes = new Float32Array(count);

    const tempColor = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const node = cortexList[i];
      positions[i * 3] = node.pos[0];
      positions[i * 3 + 1] = node.pos[1];
      positions[i * 3 + 2] = node.pos[2];

      tempColor.set(node.color || "#38bdf8");
      colors[i * 3] = tempColor.r;
      colors[i * 3 + 1] = tempColor.g;
      colors[i * 3 + 2] = tempColor.b;

      sizes[i] = 2.4;
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute("size", new THREE.BufferAttribute(sizes, 1));

    // Shader personalizado sutil o PointsMaterial de alta calidad
    const material = new THREE.PointsMaterial({
      size: 2.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    });

    this.cortexPoints = new THREE.Points(geometry, material);
    this.brainGroup.add(this.cortexPoints);
  }

  updateDynamicState(simulationState, primaryColorHex = 0x00f0ff) {
    const activations = simulationState.node_activations || {};
    const activeTracts = simulationState.active_tracts || [];

    // 1. Actualizar núcleos anatómicos (escala, emisividad y color)
    this.nucleiMeshes.forEach(mesh => {
      const nid = mesh.userData.id;
      const act = activations[nid] || 0.05;
      const baseR = mesh.userData.baseRadius;

      // Pulsación armónica proporcional a la despolarización de membrana
      const targetScale = baseR * (1.0 + act * 0.85);
      mesh.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.15);

      // Emisión luminosa
      mesh.material.emissiveIntensity = 0.25 + act * 1.5;

      if (act > 0.4) {
        // Entrando en hiperactividad sináptica
        mesh.material.color.setHex(primaryColorHex);
        mesh.material.emissive.setHex(primaryColorHex);
      } else {
        mesh.material.color.copy(mesh.userData.baseColor);
        mesh.material.emissive.copy(mesh.userData.baseColor);
      }
    });

    // 2. Actualizar manto cortical de neuronas
    if (this.cortexPoints) {
      const colors = this.cortexPoints.geometry.attributes.color.array;
      const tempColor = new THREE.Color();
      const primeColor = new THREE.Color(primaryColorHex);

      for (let i = 0; i < this.cortexData.length; i++) {
        const nid = this.cortexData[i].id;
        const act = activations[nid] || 0.05;

        if (act > 0.3) {
          tempColor.lerpColors(new THREE.Color(this.cortexData[i].color), primeColor, act);
        } else {
          tempColor.set(this.cortexData[i].color);
        }

        colors[i * 3] = tempColor.r;
        colors[i * 3 + 1] = tempColor.g;
        colors[i * 3 + 2] = tempColor.b;
      }
      this.cortexPoints.geometry.attributes.color.needsUpdate = true;
    }

    // 3. Actualizar tractografía axonal
    if (this.tractography) {
      this.tractography.updateActivations(activeTracts, primaryColorHex);
    }

    // 4. Color de la luz nuclear central
    this.coreLight.color.setHex(primaryColorHex);
  }

  checkIntersection() {
    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.nucleiMeshes);

    if (intersects.length > 0) {
      const topObj = intersects[0].object;
      if (this.intersectedObject !== topObj) {
        this.intersectedObject = topObj;
        document.body.style.cursor = "pointer";
        if (this.onNodeHover) {
          this.onNodeHover(topObj.userData, intersects[0].point);
        }
      }
    } else {
      if (this.intersectedObject !== null) {
        this.intersectedObject = null;
        document.body.style.cursor = "default";
        if (this.onNodeHover) {
          this.onNodeHover(null, null);
        }
      }
    }
  }

  setViewMode(mode) {
    this.currentViewMode = mode;
    switch (mode) {
      case "full":
        if (this.cortexPoints) this.cortexPoints.visible = true;
        this.nucleiMeshes.forEach(m => m.visible = true);
        this.tractography.setTractsVisibility(true);
        break;
      case "subcortical":
        if (this.cortexPoints) this.cortexPoints.visible = false;
        this.nucleiMeshes.forEach(m => m.visible = true);
        this.tractography.setTractsVisibility(true);
        break;
      case "tracts":
        if (this.cortexPoints) this.cortexPoints.visible = false;
        this.nucleiMeshes.forEach(m => m.visible = false);
        this.tractography.setTractsVisibility(true);
        break;
      case "transparent":
        if (this.cortexPoints) {
          this.cortexPoints.visible = true;
          this.cortexPoints.material.opacity = 0.2;
        }
        this.nucleiMeshes.forEach(m => {
          m.visible = true;
          m.material.opacity = 0.5;
        });
        this.tractography.setTractsVisibility(true);
        break;
    }
  }

  setCameraPreset(preset) {
    const target = this.controls.target;
    switch (preset) {
      case "sagittal": // Vista lateral (perfil)
        this.animateCameraTo(new THREE.Vector3(95, 0, 0), target);
        break;
      case "coronal": // Vista frontal
        this.animateCameraTo(new THREE.Vector3(0, 95, 0), target);
        break;
      case "axial": // Vista superior (dorsal)
        this.animateCameraTo(new THREE.Vector3(0, 0, 95), target);
        break;
      case "perspective":
      default:
        this.animateCameraTo(new THREE.Vector3(55, 45, 70), target);
        break;
    }
  }

  animateCameraTo(targetPos, lookTarget) {
    const startPos = this.camera.position.clone();
    let progress = 0;
    const duration = 40; // frames

    const animStep = () => {
      progress++;
      const t = progress / duration;
      const ease = t * (2 - t); // easeOutQuad
      this.camera.position.lerpVectors(startPos, targetPos, ease);
      this.controls.target.copy(lookTarget);
      if (progress < duration) {
        requestAnimationFrame(animStep);
      }
    };
    animStep();
  }

  render() {
    this.controls.update();

    // Animación suave de respiración del cerebro
    const time = performance.now() * 0.001;
    this.brainGroup.position.y = Math.sin(time * 0.8) * 0.6;

    // Actualizar pulsos de tractografía axonal
    if (this.tractography) {
      this.tractography.animate();
    }

    this.renderer.render(this.scene, this.camera);
  }
}

window.ConnectomeScene = ConnectomeScene;
