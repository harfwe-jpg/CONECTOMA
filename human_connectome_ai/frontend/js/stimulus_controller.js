/**
 * CONTROLADOR DE ESTÍMULOS NEURONALES Y SINTETIZADOR DE AUDIO (Web Audio API)
 * Administra la entrada de usuario, llamadas a la API de Python o motor de respaldo offline,
 * y genera retroalimentación acústica de disparo neuronal.
 */

class StimulusController {
  constructor(onStateUpdate) {
    this.onStateUpdate = onStateUpdate;
    this.activeStimuli = {};
    this.apiOnline = false;
    this.audioEnabled = false;
    this.audioCtx = null;
    this.masterGain = null;
    this.humOscillator = null;

    this.initAudio();
  }

  initAudio() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
        this.masterGain = this.audioCtx.createGain();
        this.masterGain.gain.value = 0.08;
        this.masterGain.connect(this.audioCtx.destination);
      }
    } catch (e) {
      console.warn("Audio no soportado o bloqueado por el navegador:", e);
    }
  }

  toggleAudio() {
    if (!this.audioCtx) return false;
    if (this.audioCtx.state === "suspended") {
      this.audioCtx.resume();
    }
    this.audioEnabled = !this.audioEnabled;

    if (this.audioEnabled) {
      this.startAmbientHum();
    } else {
      this.stopAmbientHum();
    }
    return this.audioEnabled;
  }

  startAmbientHum() {
    if (!this.audioCtx || this.humOscillator) return;
    this.humOscillator = this.audioCtx.createOscillator();
    this.humOscillator.type = "sine";
    this.humOscillator.frequency.value = 110; // 110 Hz nota A2 (tono de sincronización cerebral)
    
    this.humGain = this.audioCtx.createGain();
    this.humGain.gain.value = 0.03;
    
    this.humOscillator.connect(this.humGain);
    this.humGain.connect(this.masterGain);
    this.humOscillator.start();
  }

  stopAmbientHum() {
    if (this.humOscillator) {
      try {
        this.humOscillator.stop();
        this.humOscillator.disconnect();
      } catch (e) {}
      this.humOscillator = null;
    }
  }

  playSynapticClick(pitch = 800) {
    if (!this.audioEnabled || !this.audioCtx) return;
    try {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = "triangle";
      osc.frequency.setValueAtTime(pitch, this.audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(120, this.audioCtx.currentTime + 0.04);

      gain.gain.setValueAtTime(0.04, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.04);

      osc.connect(gain);
      gain.connect(this.masterGain);
      osc.start();
      osc.stop(this.audioCtx.currentTime + 0.04);
    } catch (e) {}
  }

  async checkApiHealth() {
    try {
      const resp = await fetch("/api/status", { cache: "no-store" });
      if (resp.ok) {
        const data = await resp.json();
        this.apiOnline = true;
        return { online: true, data };
      }
    } catch (e) {
      this.apiOnline = false;
    }
    return { online: false };
  }

  async applyStimulus(stimulusId, intensity) {
    if (intensity <= 0.01) {
      delete this.activeStimuli[stimulusId];
    } else {
      this.activeStimuli[stimulusId] = intensity;
    }

    // Audio click
    if (intensity > 0.3) {
      this.playSynapticClick(stimulusId === "excitacion" ? 1200 : stimulusId === "hambre" ? 650 : 900);
      if (this.humOscillator) {
        // Modular frecuencia según excitación
        this.humOscillator.frequency.setTargetAtTime(110 + intensity * 80, this.audioCtx.currentTime, 0.1);
      }
    }

    let stateResult = null;

    // 1. Intentar enviar a la API REST de Python
    if (this.apiOnline) {
      try {
        const resp = await fetch("/api/stimulate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ stimuli: this.activeStimuli })
        });
        if (resp.ok) {
          stateResult = await resp.json();
        }
      } catch (err) {
        console.warn("Fallo temporal comunicando con backend Python, conmutando a motor cliente:", err);
        this.apiOnline = false;
      }
    }

    // 2. Si no hay conexión al backend, calcular con motor cliente autónomo
    if (!stateResult) {
      stateResult = this.calculateLocalSimulation(this.activeStimuli);
    }

    if (this.onStateUpdate) {
      this.onStateUpdate(stateResult);
    }

    return stateResult;
  }

  calculateLocalSimulation(stimuli) {
    // Motor cliente idéntico al backend Python para respaldo 100% autónomo
    const catalog = window.STIMULI_CATALOG || {};
    const defaultConnectome = window.DEFAULT_CONNECTOME || { nodes: [], tracts: [] };

    const baselines = {
      dopamine: 0.40, serotonin: 0.60, norepinephrine: 0.30, gaba: 0.55,
      glutamate: 0.50, endorphins: 0.20, oxytocin: 0.25, ghrelin: 0.15,
      cortisol: 0.25, melatonin: 0.10
    };
    const colors = {
      dopamine: "#F59E0B", serotonin: "#10B981", norepinephrine: "#EF4444",
      gaba: "#3B82F6", glutamate: "#EC4899", endorphins: "#8B5CF6",
      oxytocin: "#F43F5E", ghrelin: "#EAB308", cortisol: "#F97316",
      melatonin: "#6366F1"
    };

    const levels = { ...baselines };
    const nodeActivations = {};
    defaultConnectome.nodes.forEach(n => { nodeActivations[n.id] = 0.05; });

    let dominantStim = null;
    let maxIntensity = 0.0;
    const narratives = [];
    const brainwaves = { delta: 0.2, theta: 0.25, alpha: 0.35, beta: 0.4, gamma: 0.3 };

    for (const [sId, intensity] of Object.entries(stimuli)) {
      if (!catalog[sId]) continue;
      const sData = catalog[sId];

      if (intensity > maxIntensity) {
        maxIntensity = intensity;
        dominantStim = sData;
      }

      // Desplazamiento neuroquímico
      for (const [nKey, shift] of Object.entries(sData.neurochemical_shifts || {})) {
        if (levels[nKey] !== undefined) {
          levels[nKey] = Math.max(0.02, Math.min(1.0, levels[nKey] + shift * intensity));
        }
      }

      // Despolarización de nodos objetivo
      for (const [nid, weight] of Object.entries(sData.target_nodes || {})) {
        if (nodeActivations[nid] !== undefined) {
          nodeActivations[nid] = Math.max(0.02, Math.min(1.0, nodeActivations[nid] + weight * intensity));
        }
      }

      // Ondas cerebrales
      for (const [wKey, pwr] of Object.entries(sData.brainwaves || {})) {
        brainwaves[wKey] += (pwr - brainwaves[wKey]) * (0.6 * intensity);
      }

      narratives.push({
        id: sId,
        name: sData.name,
        icon: sData.icon,
        intensity: intensity,
        summary: sData.summary,
        steps: sData.cascade_steps || []
      });
    }

    // Identificar tractos activos
    const activeTracts = [];
    defaultConnectome.tracts.forEach((t, idx) => {
      const srcAct = nodeActivations[t.src] || 0.0;
      const tgtAct = nodeActivations[t.tgt] || 0.0;
      const combined = (srcAct + tgtAct) / 2.0;
      if (combined > 0.25) {
        activeTracts.push({
          index: idx,
          src: t.src,
          tgt: t.tgt,
          name: t.name,
          activity: combined,
          type: t.type
        });
      }
    });

    return {
      active_stimuli: stimuli,
      dominant_stimulus: dominantStim ? dominantStim.name : "Estado Homeostático Basal",
      dominant_icon: dominantStim ? dominantStim.icon : "⚖️",
      dominant_category: dominantStim ? dominantStim.category : "Homeostasis",
      narratives: narratives,
      neurochemistry: { levels, colors },
      brainwaves: brainwaves,
      node_activations: nodeActivations,
      active_tracts: activeTracts
    };
  }

  async resetAll() {
    this.activeStimuli = {};
    if (this.humOscillator && this.audioCtx) {
      this.humOscillator.frequency.setTargetAtTime(110, this.audioCtx.currentTime, 0.2);
    }
    return await this.applyStimulus("reset", 0.0);
  }

  async runScenario(scenarioKey) {
    await this.resetAll();

    switch (scenarioKey) {
      case "dopamine_storm": // Hambre voraz + Excitación sexual simultánea
        await this.applyStimulus("hambre", 0.85);
        await this.applyStimulus("excitacion", 0.90);
        break;

      case "fight_or_flight": // Pánico + Dolor agudo
        await this.applyStimulus("miedo", 0.95);
        await this.applyStimulus("dolor", 0.80);
        break;

      case "deep_love": // Amor + Euforia
        await this.applyStimulus("amor", 0.95);
        await this.applyStimulus("euforia", 0.75);
        break;

      case "sleep_repair": // Cansancio y sueño
        await this.applyStimulus("sueno", 0.95);
        break;

      case "circadian_day": // Secuencia programada del ciclo biológico
        this.runCircadianTimeline();
        break;
    }
  }

  runCircadianTimeline() {
    const steps = [
      { time: 0, text: "07:00 AM - Despertar y Apetito Metabólico (Hambre)", stims: { "hambre": 0.8 } },
      { time: 3500, text: "10:30 AM - Trabajo Intelectual y Concentración Profunda (Flow)", stims: { "enfoque": 0.9 } },
      { time: 7000, text: "03:00 PM - Amenaza Repentina y Respuesta de Alarma (Miedo)", stims: { "miedo": 0.85 } },
      { time: 10500, text: "08:30 PM - Cita Íntima, Deseo y Conexión Erótica (Excitación + Amor)", stims: { "excitacion": 0.95, "amor": 0.8 } },
      { time: 14500, text: "11:30 PM - Transición al Reposo y Sueño Delta Profundo (VLPO activo)", stims: { "sueno": 0.9 } },
      { time: 18500, text: "Homeostasis", stims: {} }
    ];

    steps.forEach(step => {
      setTimeout(async () => {
        this.activeStimuli = {};
        for (const [k, v] of Object.entries(step.stims)) {
          await this.applyStimulus(k, v);
        }
      }, step.time);
    });
  }
}

window.StimulusController = StimulusController;
