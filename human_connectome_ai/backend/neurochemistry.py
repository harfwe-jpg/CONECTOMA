"""
Módulo de Neuroquímica - Simulación de Dinámica de Neurotransmisores y Hormonas
Representa los niveles de neuromoduladores basales y sus alteraciones por estímulos.
"""

from typing import Dict, Any

class NeurochemicalProfile:
    """Perfil neuroquímico del cerebro humano con concentraciones relativas (0.0 a 1.0)."""
    
    BASELINES = {
        "dopamine": 0.40,      # Recompensa, motivación, placer, excitación motora
        "serotonin": 0.60,     # Estado de ánimo, saciedad, calma, regulación
        "norepinephrine": 0.30,# Alerta, vigilancia, respuesta lucha/huida
        "gaba": 0.55,          # Inhibición principal, relajación, sueño
        "glutamate": 0.50,     # Excitación principal, plasticidad, cognición
        "endorphins": 0.20,    # Analgesia natural, euforia, bienestar
        "oxytocin": 0.25,      # Vínculo afectivo, empatía, orgasmo, confianza
        "ghrelin": 0.15,       # Señal de hambre (hormona péptido-gástrica)
        "cortisol": 0.25,      # Hormona del estrés, eje HPA
        "melatonin": 0.10,     # Señal circadiana de sueño
    }

    DESCRIPTIONS = {
        "dopamine": "Dopamina: Impulso motor, anticipación de recompensa y deseo.",
        "serotonin": "Serotonina: Modulación emocional, saciedad y bienestar general.",
        "norepinephrine": "Noradrenalina: Arousal simpático, alerta máxima y vigilancia.",
        "gaba": "GABA: Freno neuroquímico; inhibe la hiperactividad neuronal.",
        "glutamate": "Glutamate: Acelerador sináptico del aprendizaje y transmisión rápida.",
        "endorphins": "Endorfinas: Bloqueo nociceptivo endógeno y éxtasis sensorial.",
        "oxytocin": "Oxitocina: Neurohormona del apego, proximidad física y clímax.",
        "ghrelin": "Grelina: Señal metabólica de depleción energética / apetito.",
        "cortisol": "Cortisol: Movilización de glucosa ante amenaza o alarma.",
        "melatonin": "Melatonina: Sincronizador circadiano del núcleo supraquiasmático.",
    }

    COLORS = {
        "dopamine": "#F59E0B",       # Ámbar brillante
        "serotonin": "#10B981",      # Esmeralda sereno
        "norepinephrine": "#EF4444", # Rojo alarma
        "gaba": "#3B82F6",          # Azul índigo relajante
        "glutamate": "#EC4899",     # Magenta eléctrico
        "endorphins": "#8B5CF6",    # Púrpura euforia
        "oxytocin": "#F43F5E",      # Rosa afectivo
        "ghrelin": "#EAB308",       # Amarillo visceral
        "cortisol": "#F97316",      # Naranja estrés
        "melatonin": "#6366F1",     # Violeta nocturno
    }

    def __init__(self):
        self.levels = dict(self.BASELINES)

    def reset_to_baseline(self):
        self.levels = dict(self.BASELINES)

    def apply_modulation(self, deltas: Dict[str, float], intensity: float = 1.0, decay_rate: float = 0.05):
        """Aplica cambios a los niveles y asegura que permanezcan en [0.0, 1.0]."""
        for neuro, target_delta in deltas.items():
            if neuro in self.levels:
                effective_shift = target_delta * intensity
                # Mezcla hacia el nuevo nivel objetivo
                current = self.levels[neuro]
                self.levels[neuro] = max(0.02, min(1.0, current + effective_shift))

    def decay_towards_baseline(self, rate: float = 0.08):
        """Regresa suavemente hacia el estado homeostático."""
        for neuro, baseline in self.BASELINES.items():
            current = self.levels[neuro]
            self.levels[neuro] += (baseline - current) * rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "levels": {k: round(v, 4) for k, v in self.levels.items()},
            "colors": self.COLORS,
            "descriptions": self.DESCRIPTIONS
        }
