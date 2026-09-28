/**
 * ORQUESTADOR PRINCIPAL DE LA APLICACIÓN (Main Entry Point)
 * Inicializa la visualización 3D, el HUD neuroquímico y enlaza los controladores.
 */

document.addEventListener("DOMContentLoaded", async () => {
  const canvas = document.getElementById("connectome-canvas");
  const statusPill = document.getElementById("backend-status-pill");
  const statusText = document.getElementById("backend-status-text");
  const audioToggleBtn = document.getElementById("btn-audio-toggle");
  const resetBtn = document.getElementById("btn-reset-all");

  // 1. Instanciar HUD
  const hud = new HudOverlay();

  // 2. Instanciar Escena Three.js
  const scene = new ConnectomeScene(
    canvas,
    // Callback hover
    (nodeData, pt) => {
      hud.showInspector(nodeData);
      if (nodeData && pt) {
        // Proyectar 3D a pantalla 2D para tooltip
        const p = pt.clone().project(scene.camera);
        const x = (p.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-(p.y * 0.5) + 0.5) * window.innerHeight;
        hud.showTooltip(nodeData, { x, y });
      } else {
        hud.showTooltip(null, null);
      }
    },
    // Callback click
    (nodeData) => {
      if (nodeData) {
        hud.showInspector(nodeData);
      }
    }
  );

  // 3. Determinar color primario de resplandor según estímulo
  function getStimulusColor(state) {
    if (!state || !state.active_stimuli) return 0x00f0ff;
    const stims = state.active_stimuli;
    if (stims.excitacion) return 0xf43f5e; // Rosa carmín erótico
    if (stims.hambre) return 0xf59e0b;     // Ámbar apetitivo
    if (stims.miedo) return 0xef4444;      // Rojo peligro
    if (stims.dolor) return 0xec4899;      // Magenta dolor
    if (stims.sueno) return 0x6366f1;      // Índigo sueño
    if (stims.enfoque) return 0x00f0ff;    // Cian cognitivo
    if (stims.amor) return 0xf43f5e;       // Rosa amor
    if (stims.euforia) return 0xfbbf24;    // Dorado triunfo
    return 0x00f0ff;
  }

  // 4. Instanciar Controlador de Estímulos
  const stimController = new StimulusController((newState) => {
    const colorHex = getStimulusColor(newState);
    scene.updateDynamicState(newState, colorHex);
    hud.updateState(newState);
    updateStatsCounter(newState);
  });

  // 5. Cargar Conectoma (Backend API o Respaldo local)
  let connectomeData = null;
  const health = await stimController.checkApiHealth();

  if (health.online) {
    if (statusPill) statusPill.style.borderColor = "var(--color-emerald)";
    if (statusText) statusText.textContent = "API PYTHON: ONLINE";
    try {
      const resp = await fetch("/api/connectome");
      connectomeData = await resp.json();
    } catch (e) {
      console.warn("Error cargando conectoma por API, usando fallback:", e);
    }
  } else {
    if (statusPill) statusPill.style.borderColor = "var(--color-amber)";
    if (statusText) statusText.textContent = "CLIENTE 3D: AUTÓNOMO";
  }

  if (!connectomeData && window.DEFAULT_CONNECTOME) {
    connectomeData = window.DEFAULT_CONNECTOME;
  }

  if (connectomeData) {
    scene.loadConnectome(connectomeData);
  }

  // 6. Estado inicial homeostático
  const initialState = await stimController.applyStimulus("reset", 0.0);

  // 7. Enlazar Sliders y Botones de Estímulo
  bindStimulusControls(stimController);

  // 8. Enlazar Presets y Escenarios
  bindPresetButtons(stimController);

  // 9. Enlazar Modos de Visualización y Vistas de Cámara
  bindViewButtons(scene);

  // 10. Controles de Audio y Reset
  if (audioToggleBtn) {
    audioToggleBtn.addEventListener("click", () => {
      const enabled = stimController.toggleAudio();
      audioToggleBtn.classList.toggle("active", enabled);
      audioToggleBtn.innerHTML = enabled
        ? '<i class="fas fa-volume-up"></i> AUDIO: ON'
        : '<i class="fas fa-volume-mute"></i> AUDIO: OFF';
    });
  }

  if (resetBtn) {
    resetBtn.addEventListener("click", async () => {
      // Reset de todos los sliders visuales
      document.querySelectorAll(".stimulus-slider").forEach(sl => {
        sl.value = 0;
        const valSpan = sl.parentElement.querySelector(".slider-val");
        if (valSpan) valSpan.textContent = "0%";
      });
      document.querySelectorAll(".stimulus-card").forEach(c => {
        c.className = "stimulus-card";
      });
      await stimController.resetAll();
    });
  }

  // 11. Loop Principal de Renderizado (RAF)
  function renderLoop() {
    requestAnimationFrame(renderLoop);
    scene.render();
    hud.animateEEG();
  }
  renderLoop();
});

// Enlazar controles de la barra lateral izquierda
function bindStimulusControls(stimController) {
  const sliders = document.querySelectorAll(".stimulus-slider");

  sliders.forEach(slider => {
    const stimId = slider.dataset.stimulus;
    const card = slider.closest(".stimulus-card");
    const valDisplay = slider.parentElement.querySelector(".slider-val");

    slider.addEventListener("input", async (e) => {
      const val = parseFloat(e.target.value) / 100.0;
      if (valDisplay) valDisplay.textContent = `${Math.round(val * 100)}%`;

      // Clases activas según tipo
      if (val > 0.05) {
        card.classList.add("active");
        if (stimId === "hambre") card.classList.add("active-hunger");
        if (stimId === "excitacion") card.classList.add("active-arousal");
        if (stimId === "miedo") card.classList.add("active-fear");
      } else {
        card.className = "stimulus-card";
      }

      await stimController.applyStimulus(stimId, val);
    });
  });

  // Botones de disparo rápido / pulso
  document.querySelectorAll(".btn-pulse").forEach(btn => {
    btn.addEventListener("click", async () => {
      const stimId = btn.dataset.stimulus;
      const targetIntensity = parseFloat(btn.dataset.intensity || "0.9");
      const slider = document.querySelector(`.stimulus-slider[data-stimulus="${stimId}"]`);
      if (slider) {
        slider.value = targetIntensity * 100;
        slider.dispatchEvent(new Event("input"));
      }
    });
  });
}

// Enlazar botones de escenarios automáticos
function bindPresetButtons(stimController) {
  document.querySelectorAll(".btn-preset").forEach(btn => {
    btn.addEventListener("click", async () => {
      const scenarioKey = btn.dataset.scenario;
      await stimController.runScenario(scenarioKey);
      
      // Sincronizar sliders si aplican
      if (scenarioKey === "dopamine_storm") {
        setSliderVal("hambre", 85);
        setSliderVal("excitacion", 90);
      } else if (scenarioKey === "fight_or_flight") {
        setSliderVal("miedo", 95);
        setSliderVal("dolor", 80);
      } else if (scenarioKey === "deep_love") {
        setSliderVal("amor", 95);
        setSliderVal("euforia", 75);
      } else if (scenarioKey === "sleep_repair") {
        setSliderVal("sueno", 95);
      }
    });
  });
}

function setSliderVal(stimId, valPct) {
  const slider = document.querySelector(`.stimulus-slider[data-stimulus="${stimId}"]`);
  if (slider) {
    slider.value = valPct;
    const card = slider.closest(".stimulus-card");
    const valDisplay = slider.parentElement.querySelector(".slider-val");
    if (valDisplay) valDisplay.textContent = `${valPct}%`;
    if (card) card.classList.add("active");
  }
}

// Enlazar vistas de cámara y modos de visualización
function bindViewButtons(scene) {
  document.querySelectorAll(".btn-view[data-view]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".btn-view[data-view]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      scene.setViewMode(btn.dataset.view);
    });
  });

  document.querySelectorAll(".btn-view[data-camera]").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".btn-view[data-camera]").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      scene.setCameraPreset(btn.dataset.camera);
    });
  });
}

// Contador estadístico en el pie de página
function updateStatsCounter(state) {
  const nodesEl = document.getElementById("stat-active-nodes");
  const tractsEl = document.getElementById("stat-active-tracts");
  const firingEl = document.getElementById("stat-firing-rate");

  if (state) {
    if (tractsEl && state.active_tracts) {
      tractsEl.textContent = state.active_tracts.length;
    }
    if (nodesEl && state.node_activations) {
      const activeCount = Object.values(state.node_activations).filter(v => v > 0.3).length;
      nodesEl.textContent = activeCount;
    }
    if (firingEl) {
      let totalStim = 0;
      for (const v of Object.values(state.active_stimuli || {})) totalStim += v;
      const hz = Math.round(15 + totalStim * 75);
      firingEl.textContent = `${hz} Hz`;
    }
  }
}
