/**
 * HUD & TELEMETRÍA NEUROLÓGICA (Osciloscopio EEG, Neuroquímica, Inspector Anatómico)
 * Actualiza en tiempo real los paneles bidireccionales de visualización de datos.
 */

class HudOverlay {
  constructor() {
    this.eegCanvas = document.getElementById("eeg-canvas");
    this.eegCtx = this.eegCanvas ? this.eegCanvas.getContext("2d") : null;
    this.waveHistory = new Array(180).fill(0);
    this.waveTime = 0;

    this.neuroListContainer = document.getElementById("neuro-list");
    this.narrativeContainer = document.getElementById("narrative-box");
    this.inspectorCard = document.getElementById("inspector-card");
    this.stateBanner = document.getElementById("state-banner");
    this.brainTooltip = document.getElementById("brain-tooltip");

    this.currentBrainwaves = { delta: 0.2, theta: 0.25, alpha: 0.35, beta: 0.4, gamma: 0.3 };
  }

  updateState(state) {
    if (!state) return;

    // 1. Banner de Estado Dominante
    if (this.stateBanner) {
      const iconEl = this.stateBanner.querySelector(".state-icon");
      const catEl = this.stateBanner.querySelector(".state-category");
      const titleEl = this.stateBanner.querySelector(".state-title");

      if (iconEl) iconEl.textContent = state.dominant_icon || "🧠";
      if (catEl) catEl.textContent = state.dominant_category || "HOMEOSTASIS";
      if (titleEl) titleEl.textContent = state.dominant_stimulus || "Estado Homeostático Basal";
    }

    // 2. Ondas Cerebrales (EEG)
    if (state.brainwaves) {
      this.currentBrainwaves = state.brainwaves;
      this.updateBrainwaveBars(state.brainwaves);
    }

    // 3. Neuroquímica (Dopamina, Serotonina, Oxitocina, Grelina, etc.)
    if (state.neurochemistry && state.neurochemistry.levels) {
      this.updateNeurochemistryGauges(state.neurochemistry);
    }

    // 4. Narrativa Neurobiológica de la Cascada Sináptica
    if (state.narratives && state.narratives.length > 0) {
      this.updateNarrative(state.narratives);
    } else {
      if (this.narrativeContainer) {
        this.narrativeContainer.innerHTML = `
          <div class="narrative-step">
            <strong>Homeostasis Neurovegetativa:</strong> El encéfalo mantiene potenciales de membrana en reposo basal (-70mV). Los núcleos dopaminérgicos y serotoninérgicos operan a frecuencias tónicas de equilibrio.
          </div>
        `;
      }
    }
  }

  updateBrainwaveBars(waves) {
    const waveKeys = ["delta", "theta", "alpha", "beta", "gamma"];
    waveKeys.forEach(key => {
      const fillEl = document.getElementById(`wave-bar-${key}`);
      const val = waves[key] || 0.1;
      if (fillEl) {
        fillEl.style.width = `${Math.min(100, Math.round(val * 100))}%`;
      }
    });
  }

  updateNeurochemistryGauges(neuroData) {
    if (!this.neuroListContainer) return;

    const levels = neuroData.levels;
    const colors = neuroData.colors || {};

    const nameMap = {
      dopamine: "Dopamina",
      serotonin: "Serotonina",
      norepinephrine: "Noradrenalina",
      oxytocin: "Oxitocina",
      endorphins: "Endorfinas",
      ghrelin: "Grelina (Hambre)",
      cortisol: "Cortisol (Estrés)",
      gaba: "GABA (Freno)",
      glutamate: "Glutamato",
      melatonin: "Melatonina (Sueño)"
    };

    let html = "";
    for (const [key, val] of Object.entries(levels)) {
      const displayName = nameMap[key] || key;
      const pct = Math.min(100, Math.round(val * 100));
      const color = colors[key] || "#00f0ff";

      html += `
        <div class="neuro-row" title="${neuroData.descriptions ? neuroData.descriptions[key] : ''}">
          <div class="neuro-name">${displayName}</div>
          <div class="neuro-bar-track">
            <div class="neuro-bar-fill" style="width: ${pct}%; background-color: ${color}; box-shadow: 0 0 8px ${color}88;"></div>
          </div>
          <div class="neuro-val">${pct}%</div>
        </div>
      `;
    }
    this.neuroListContainer.innerHTML = html;
  }

  updateNarrative(narratives) {
    if (!this.narrativeContainer) return;

    let html = "";
    narratives.forEach(item => {
      html += `
        <div style="margin-bottom: 10px; border-bottom: 1px dashed rgba(255,255,255,0.08); padding-bottom: 6px;">
          <div style="color: #fff; font-weight: 600; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
            <span>${item.icon}</span> <span>${item.name} (${Math.round(item.intensity * 100)}%)</span>
          </div>
          <div style="font-size: 10px; color: #94a3b8; margin-bottom: 6px;">${item.summary}</div>
          ${item.steps.map(s => `<div class="narrative-step">${s}</div>`).join("")}
        </div>
      `;
    });
    this.narrativeContainer.innerHTML = html;
  }

  showInspector(nodeData) {
    if (!this.inspectorCard) return;

    if (!nodeData) {
      this.inspectorCard.classList.remove("active");
      return;
    }

    this.inspectorCard.classList.add("active");
    const titleEl = this.inspectorCard.querySelector(".inspector-title");
    const metaEl = this.inspectorCard.querySelector(".inspector-meta");
    const descEl = this.inspectorCard.querySelector(".inspector-desc");

    if (titleEl) titleEl.textContent = `${nodeData.name} [${nodeData.id}]`;
    if (metaEl) {
      const posStr = `MNI 3D: [${nodeData.pos ? nodeData.pos.join(", ") : ""}]`;
      const transStr = nodeData.transmitters ? ` | Neurotransmisores: ${nodeData.transmitters.join(", ")}` : "";
      metaEl.textContent = `${posStr}${transStr}`;
    }
    if (descEl) descEl.textContent = nodeData.desc || "Estructura de interconexión sináptica cerebral.";
  }

  showTooltip(nodeData, screenPos) {
    if (!this.brainTooltip) return;
    if (!nodeData || !screenPos) {
      this.brainTooltip.style.display = "none";
      return;
    }

    this.brainTooltip.style.display = "block";
    this.brainTooltip.style.left = `${screenPos.x}px`;
    this.brainTooltip.style.top = `${screenPos.y}px`;
    this.brainTooltip.innerHTML = `<strong>${nodeData.name}</strong><br><span style="color:#00f0ff; font-size:10px;">${nodeData.group || 'Cerebro'}</span>`;
  }

  animateEEG() {
    if (!this.eegCtx || !this.eegCanvas) return;

    const ctx = this.eegCtx;
    const w = this.eegCanvas.width;
    const h = this.eegCanvas.height;
    const midY = h / 2;

    this.waveTime += 0.05;

    // Calcular amplitud compuesta sintetizando frecuencias biológicas
    const bw = this.currentBrainwaves;
    const delta = Math.sin(this.waveTime * 0.8) * (bw.delta * 22);
    const theta = Math.sin(this.waveTime * 2.2) * (bw.theta * 14);
    const alpha = Math.sin(this.waveTime * 4.5) * (bw.alpha * 10);
    const beta = Math.sin(this.waveTime * 9.0 + Math.cos(this.waveTime * 3.0)) * (bw.beta * 7);
    const gamma = (Math.random() - 0.5) * (bw.gamma * 8);

    const currentSample = delta + theta + alpha + beta + gamma;

    // Rotar buffer de muestras
    this.waveHistory.shift();
    this.waveHistory.push(currentSample);

    // Dibujar en canvas
    ctx.fillStyle = "rgba(5, 10, 16, 0.4)";
    ctx.fillRect(0, 0, w, h);

    // Rejilla de osciloscopio
    ctx.strokeStyle = "rgba(0, 240, 255, 0.08)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, midY);
    ctx.lineTo(w, midY);
    ctx.stroke();

    // Trazado de señal EEG fosforescente
    ctx.strokeStyle = "#00f0ff";
    ctx.shadowColor = "#00f0ff";
    ctx.shadowBlur = 6;
    ctx.lineWidth = 1.8;
    ctx.beginPath();

    const stepX = w / (this.waveHistory.length - 1);
    for (let i = 0; i < this.waveHistory.length; i++) {
      const x = i * stepX;
      const y = midY - this.waveHistory[i];
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    }
    ctx.stroke();
    ctx.shadowBlur = 0; // Reset
  }
}

window.HudOverlay = HudOverlay;
