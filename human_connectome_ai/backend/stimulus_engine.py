"""
Motor de Dinámica Neuronal de Estímulos Corporales Humanos
Simula la propagación de potenciales de acción, despolarización de membrana,
cambios neuroendocrinos y ondas cerebrales (EEG) ante estímulos corporales vitales.
"""

import math
from typing import Dict, List, Any
try:
    from backend.neurochemistry import NeurochemicalProfile
    from backend.connectome_model import BrainConnectome
except ImportError:
    from neurochemistry import NeurochemicalProfile
    from connectome_model import BrainConnectome

class StimulusEngine:
    """Motor neuro-computacional que procesa estímulos somáticos y emocionales."""

    STIMULI_CATALOG = {
        "hambre": {
            "name": "Hambre y Apetito Metabólico",
            "category": "Homeostático / Supervivencia",
            "icon": "🍗",
            "summary": "Cascada de privación calórica: del nervio vago al eje Hipotálamo Lateral - Núcleo Accumbens.",
            "description": "Ante el descenso de glucosa y contracciones gástricas, el estómago secreta Grelina. La aferencia del nervio vago ingresa por el Núcleo del Tracto Solitario (NTS) e hiperactiva las neuronas orexinérgicas del Hipotálamo Lateral. La Ínsula proyecta la sensación visceral de vacío, mientras el VTA envía dopamina al Núcleo Accumbens generando una urgencia motivacional obsesiva ('wanting') de buscar alimento rico en calorías.",
            "target_nodes": {
                "NTS_SOLITARY": 0.95,
                "HYPO_LH": 1.0,
                "INSULA_L": 0.88,
                "INSULA_R": 0.88,
                "NACC_L": 0.82,
                "NACC_R": 0.82,
                "OFC_L": 0.78,
                "OFC_R": 0.78,
                "DLPFC_L": 0.65,
                "HYPO_VMH": -0.85  # Inhibición del centro de saciedad
            },
            "neurochemical_shifts": {
                "ghrelin": 0.75,
                "dopamine": 0.35,
                "serotonin": -0.35,
                "cortisol": 0.22,
                "norepinephrine": 0.25,
                "gaba": -0.15
            },
            "brainwaves": {"delta": 0.15, "theta": 0.45, "alpha": 0.25, "beta": 0.65, "gamma": 0.40},
            "cascade_steps": [
                "1. Secreción periférica de Grelina y mecanorreceptores gástricos disparan por el Nervio Vago al Núcleo del Tracto Solitario (NTS).",
                "2. Transmisión axónica inmediata al Hipotálamo Lateral (HYPO_LH): liberación masiva de Orexina y Neuropéptido Y.",
                "3. La Corteza Insular (Ínsula) decodifica la propiocepción visceral: 'tengo hambre, el estómago está vacío'.",
                "4. El Área Tegmental Ventral (VTA) inunda de dopamina al Núcleo Accumbens: se activa el estado de apetencia e impulsividad.",
                "5. La Corteza Orbitofrontal (OFC) simula sabores y aromas placenteros para dirigir la búsqueda motora voluntaria."
            ]
        },

        "excitacion": {
            "name": "Excitación Sexual, Deseo y Clímax",
            "category": "Reproductivo / Hedónico",
            "icon": "🔥",
            "summary": "Circuito del deseo erótico: activación masiva del Área Preóptica Medial, Núcleo Accumbens e hipofrontalidad.",
            "description": "Se inicia por estímulos sensoriales táctiles, visuales o pensamientos eróticos. Se produce una potente despolarización en el Área Preóptica Medial (MPOA) del hipotálamo, que estimula al VTA para verter cantidades astronómicas de Dopamina en el Núcleo Accumbens. Simultáneamente ocurre una 'hipofrontalidad transitoria': la Corteza Prefrontal (DLPFC) reduce su actividad inhibitoria, suspendiendo el pudor, la timidez y la autocrítica. Durante el clímax se desatan cascadas de Oxitocina y Endorfinas generando placer orgásmico intenso.",
            "target_nodes": {
                "HYPO_MPOA": 1.0,
                "VTA": 0.98,
                "NACC_L": 0.96,
                "NACC_R": 0.96,
                "AMYG_L": 0.84,
                "AMYG_R": 0.84,
                "S1_L": 0.92,
                "S1_R": 0.92,
                "INSULA_L": 0.86,
                "INSULA_R": 0.86,
                "HYPO_PVN": 0.90,
                "ACC": 0.72,
                "OFC_L": 0.88,
                "OFC_R": 0.88,
                "DLPFC_L": -0.70,  # Hipofrontalidad transitoria: pérdida de control inhibitorio
                "DLPFC_R": -0.70
            },
            "neurochemical_shifts": {
                "dopamine": 0.80,
                "oxytocin": 0.70,
                "endorphins": 0.65,
                "norepinephrine": 0.45,
                "serotonin": -0.20,
                "glutamate": 0.50
            },
            "brainwaves": {"delta": 0.10, "theta": 0.35, "alpha": 0.20, "beta": 0.55, "gamma": 0.85},
            "cascade_steps": [
                "1. Integración sensorial tálamo-cortical (V1 y Corteza Somatosensorial S1): percepción de estímulos eróticos y tacto sensible.",
                "2. Activación del Área Preóptica Medial del Hipotálamo (MPOA): switch biológico central de la receptividad y apetito sexual.",
                "3. Estallido dopaminérgico mesolímbico (VTA -> Núcleo Accumbens bilateral): euforia anticipatoria, excitación corporal y erección/lubricación autonómica.",
                "4. Hipofrontalidad Prefrontal (DLPFC se apaga parcialmente): suspensión del análisis crítico, control racional y timidez.",
                "5. Liberación en oleadas de Oxitocina (HYPO_PVN) y Endorfinas endógenas al aproximarse el clímax orgásmico."
            ]
        },

        "miedo": {
            "name": "Miedo y Respuesta Lucha o Huida",
            "category": "Defensivo / Urgencia",
            "icon": "⚡",
            "summary": "Alarma amigdalina subcortical ultrarrápida (12 ms) y descarga de Noradrenalina por el Locus Coeruleus.",
            "description": "Una amenaza percibida viaja por la vía rápida del Tálamo directo a la Amígdala basolateral evitando la corteza consciente. La Amígdala descarga sobre el Locus Coeruleus liberando una tormenta de Noradrenalina y sobre el núcleo paraventricular para el eje del Cortisol (estrés). El corazón late desbocado, los músculos se tensan (M1) y el cerebro entra en estado de hipervigilancia de supervivencia.",
            "target_nodes": {
                "AMYG_L": 1.0,
                "AMYG_R": 1.0,
                "LOCUS_COERULEUS": 0.98,
                "HYPO_PVN": 0.92,
                "ACC": 0.88,
                "THAL_L": 0.80,
                "THAL_R": 0.80,
                "M1_L": 0.85,
                "M1_R": 0.85,
                "DLPFC_L": -0.35
            },
            "neurochemical_shifts": {
                "norepinephrine": 0.85,
                "cortisol": 0.78,
                "glutamate": 0.65,
                "gaba": -0.45,
                "serotonin": -0.30
            },
            "brainwaves": {"delta": 0.05, "theta": 0.20, "alpha": 0.15, "beta": 0.85, "gamma": 0.75},
            "cascade_steps": [
                "1. Vía tálamo-amigdalina ultracorta: detección inconsciente del peligro en 12 milisegundos.",
                "2. Núcleo central de la amígdala activa el Locus Coeruleus: torrente encefálico y periférico de Noradrenalina.",
                "3. El Hipotálamo Paraventricular dispara el eje HPA: secreción masiva de Cortisol para movilizar glucosa sanguínea.",
                "4. Corteza Motora Primaria (M1) entra en hipertono postural de combate o carrera evasiva.",
                "5. La Corteza Cingulada Anterior (ACC) experimenta angustia aguda y aprehensión de peligro inminente."
            ]
        },

        "dolor": {
            "name": "Dolor Agudo y Nocicepción",
            "category": "Somatosensorial / Protección",
            "icon": "🩸",
            "summary": "Haz espinotalámico hacia el tálamo, corteza somatosensorial S1 y cingulada anterior (sufrimiento).",
            "description": "Las fibras nociceptivas A-delta y C proyectan a través de la médula espinal hacia los núcleos VPL del Tálamo. El Tálamo proyecta doblemente: a la corteza somatosensorial S1 (que ubica con precisión milimétrica el sitio de la herida) y a la Corteza Cingulada Anterior (ACC) y la Ínsula, que codifican el sufrimiento y la angustia psicológica del dolor.",
            "target_nodes": {
                "THAL_L": 0.96,
                "THAL_R": 0.96,
                "S1_L": 0.98,
                "S1_R": 0.98,
                "ACC": 1.0,
                "INSULA_L": 0.90,
                "INSULA_R": 0.90,
                "AMYG_L": 0.75,
                "M1_L": 0.70
            },
            "neurochemical_shifts": {
                "glutamate": 0.80,
                "endorphins": 0.40,  # Intento de analgesia endógena
                "cortisol": 0.45,
                "norepinephrine": 0.50,
                "serotonin": -0.25
            },
            "brainwaves": {"delta": 0.10, "theta": 0.30, "alpha": 0.20, "beta": 0.80, "gamma": 0.65},
            "cascade_steps": [
                "1. Fibras nociceptivas ascienden por el haz espinotalámico hasta los núcleos de relevo del Tálamo.",
                "2. La Corteza Somatosensorial (S1) localiza topográficamente la agresión física e intensidad.",
                "3. La Corteza Cingulada Anterior (ACC) genera el componente subjetivo afectivo de sufrimiento e intolerancia.",
                "4. La Ínsula procesa el malestar visceral y la reacción neurovegetativa autonómica.",
                "5. Sistema opioide endógeno activa liberación reactiva de Endorfinas para atenuar la descarga sináptica dolorosa."
            ]
        },

        "enfoque": {
            "name": "Enfoque Cognitivo, Concentración y Flow",
            "category": "Cognitivo / Ejecutivo",
            "icon": "🧠",
            "summary": "Red frontoparietal ejecutiva activada: corteza prefrontal dorsolateral en sincronía con el cíngulo.",
            "description": "Durante la concentración profunda en una tarea compleja, la Corteza Prefrontal Dorsolateral (DLPFC) se sincroniza con la Corteza Cingulada Anterior para suprimir distractores externos e internos. Se apaga la Red Neuronal por Defecto (DMN, ensoñación despierta). Niveles tónicos y equilibrados de Dopamina y Noradrenalina estabilizan la memoria operativa sin ansiedad.",
            "target_nodes": {
                "DLPFC_L": 1.0,
                "DLPFC_R": 1.0,
                "ACC": 0.85,
                "THAL_L": 0.65,
                "THAL_R": 0.65,
                "M1_L": 0.40,
                "AMYG_L": -0.60, # Apagado de alarma emocional
                "AMYG_R": -0.60
            },
            "neurochemical_shifts": {
                "dopamine": 0.45,
                "norepinephrine": 0.35,
                "glutamate": 0.55,
                "gaba": 0.35,
                "cortisol": -0.15
            },
            "brainwaves": {"delta": 0.05, "theta": 0.25, "alpha": 0.30, "beta": 0.75, "gamma": 0.70},
            "cascade_steps": [
                "1. Activación de la red fronto-parietal de control atencional centrada en la Corteza Prefrontal Dorsolateral (DLPFC).",
                "2. Supresión activa de la red en modo por defecto (DMN) y silenciamiento de rumiaciones emocionales amigdalinas.",
                "3. La Corteza Cingulada Anterior supervisa la detección de errores y el ajuste dinámico del esfuerzo cognitivo.",
                "4. Liberación fásica controlada de Dopamina y Acetilcolina optimiza la relación señal/ruido en las neuronas piramidales.",
                "5. Sincronización oscilatoria en bandas Beta y Gamma sobre la corteza asociativa."
            ]
        },

        "sueno": {
            "name": "Sueño Profundo y Cansancio Extremo",
            "category": "Reparador / Circadiano",
            "icon": "🌙",
            "summary": "Interruptor VLPO activado, apagado GABAérgico de vigilia y secreción de melatonina pineal.",
            "description": "La acumulación de adenosina en el prosencéfalo basal activa el Núcleo Preóptico Ventrolateral (VLPO). El VLPO dispara proyecciones inhibidoras de GABA y Galanina que apagan secuencialmente a los centros de vigilia: el Locus Coeruleus, los núcleos de histamina y el VTA. La Glándula Pineal eleva la Melatonina en la oscuridad. Las ondas cerebrales caen en oscilaciones lentas Delta (0.5 a 4 Hz).",
            "target_nodes": {
                "VLPO": 1.0,
                "PINEAL": 0.95,
                "LOCUS_COERULEUS": -0.85, # Silenciado
                "VTA": -0.75,            # Silenciado
                "HYPO_LH": -0.85,        # Orexina apagada
                "DLPFC_L": -0.85,        # Corteza pensante apagada
                "DLPFC_R": -0.85,
                "S1_L": -0.60
            },
            "neurochemical_shifts": {
                "melatonin": 0.85,
                "gaba": 0.80,
                "dopamine": -0.55,
                "norepinephrine": -0.65,
                "cortisol": -0.50,
                "serotonin": 0.30
            },
            "brainwaves": {"delta": 0.90, "theta": 0.65, "alpha": 0.20, "beta": 0.10, "gamma": 0.05},
            "cascade_steps": [
                "1. La presión homeostática de sueño (acumulación de Adenosina) activa el Núcleo Preóptico Ventrolateral (VLPO).",
                "2. La Glándula Pineal incrementa la descarga neuroendocrina de Melatonina sincronizando el reloj biológico.",
                "3. Descarga masiva inhibitoria de GABA y Galanina desde el VLPO hacia los núcleos monoaminérgicos del tronco encéfalo.",
                "4. Se apagan el Locus Coeruleus y los centros de alerta; colapso de la afluencia sensorial hacia la corteza.",
                "5. Sincronización tálamo-cortical lenta: irrupción de ondas Delta reparadoras y consolidación de memoria nocturna."
            ]
        },

        "amor": {
            "name": "Amor, Apego Afectivo y Empatía",
            "category": "Social / Vínculo",
            "icon": "💖",
            "summary": "Cascada de Oxitocina y Dopamina: desactivación del miedo social amigdalino y confianza biológica.",
            "description": "La interacción íntima y afectuosa desencadena la síntesis masiva de Oxitocina y Vasopresina en el Núcleo Paraventricular del Hipotálamo. Estas neurohormonas inundan el Núcleo Accumbens y la Corteza Cingulada Anterior, produciendo calidez, reducción de la desconfianza (inhibición de la Amígdala) y apego duradero.",
            "target_nodes": {
                "HYPO_PVN": 0.95,
                "NACC_L": 0.88,
                "NACC_R": 0.88,
                "VTA": 0.82,
                "AMYG_L": -0.65, # Desactiva el juicio negativo y recelo social
                "AMYG_R": -0.65,
                "INSULA_L": 0.75,
                "INSULA_R": 0.75,
                "ACC": 0.80
            },
            "neurochemical_shifts": {
                "oxytocin": 0.85,
                "dopamine": 0.55,
                "endorphins": 0.60,
                "serotonin": 0.45,
                "cortisol": -0.45,
                "norepinephrine": 0.10
            },
            "brainwaves": {"delta": 0.15, "theta": 0.40, "alpha": 0.60, "beta": 0.35, "gamma": 0.45},
            "cascade_steps": [
                "1. Proximidad afectiva, contacto visual o caricias estimulan el Núcleo Paraventricular (HYPO_PVN).",
                "2. Oleada neuroendocrina de Oxitocina en el sistema límbico: suprime la reactividad de la Amígdala defensiva.",
                "3. El VTA y el Núcleo Accumbens liberan dopamina vinculada a la persona amada, consolidando el lazo de apego.",
                "4. La Corteza Insular registra sensaciones profundas de calma, calidez visceral y seguridad interpersonal.",
                "5. Descenso acentuado de Cortisol: desvanecimiento del estrés crónico y relajación fisiológica."
            ]
        },

        "euforia": {
            "name": "Euforia, Victoria y Recompensa Extrema",
            "category": "Hedónico / Triunfo",
            "icon": "🏆",
            "summary": "Disparo hiperdopaminérgico en VTA y Núcleo Accumbens con liberación de endorfinas.",
            "description": "Lograr una meta largamente anhelada, ganar un desafío o vivir una experiencia de éxtasis desata una ráfaga sincrónica desde el VTA hacia todo el estriado ventral y corteza orbitofrontal. Se experimenta invulnerabilidad, gozo expansivo y vigor motor vigoroso.",
            "target_nodes": {
                "VTA": 1.0,
                "NACC_L": 1.0,
                "NACC_R": 1.0,
                "OFC_L": 0.92,
                "OFC_R": 0.92,
                "M1_L": 0.75,
                "M1_R": 0.75,
                "ACC": 0.85
            },
            "neurochemical_shifts": {
                "dopamine": 0.90,
                "endorphins": 0.85,
                "serotonin": 0.50,
                "norepinephrine": 0.40,
                "gaba": 0.20
            },
            "brainwaves": {"delta": 0.05, "theta": 0.20, "alpha": 0.40, "beta": 0.70, "gamma": 0.90},
            "cascade_steps": [
                "1. Reconocimiento de recompensa extraordinaria o logro vital en la Corteza Orbitofrontal.",
                "2. Activación al 100% de las neuronas dopaminérgicas del VTA con descarga explosiva en el Núcleo Accumbens.",
                "3. Inundación de Endorfinas que producen una sensación de éxtasis, analgesia y plenitud.",
                "4. Activación enérgica de la Corteza Motora Primaria (expresiones de júbilo y dinamismo físico).",
                "5. Resonancia en altas frecuencias Gamma en circuitos fronto-límbicos."
            ]
        }
    }

    def __init__(self, connectome: BrainConnectome):
        self.connectome = connectome
        self.neurochemistry = NeurochemicalProfile()
        self.current_activations: Dict[str, float] = {nid: 0.05 for nid in connectome.nodes_data}
        self.current_active_stimuli: Dict[str, float] = {}  # {stimulus_id: intensity}
        self.current_step_index = 0

    def stimulate(self, stimulus_ids: Dict[str, float]) -> Dict[str, Any]:
        """
        Aplica uno o múltiples estímulos con intensidades variables (0.0 a 1.0)
        y calcula el estado sináptico y neuroquímico integrado.
        """
        self.current_active_stimuli = {k: min(1.0, max(0.0, v)) for k, v in stimulus_ids.items() if v > 0.01}
        
        # Reset de niveles base
        self.neurochemistry.reset_to_baseline()
        integrated_node_targets = {nid: 0.05 for nid in self.connectome.nodes_data}
        integrated_brainwaves = {"delta": 0.2, "theta": 0.25, "alpha": 0.35, "beta": 0.4, "gamma": 0.3}
        active_narratives = []
        dominant_stimulus = None
        max_stim_intensity = 0.0

        for stim_id, intensity in self.current_active_stimuli.items():
            if stim_id not in self.STIMULI_CATALOG:
                continue

            stim_data = self.STIMULI_CATALOG[stim_id]
            if intensity > max_stim_intensity:
                max_stim_intensity = intensity
                dominant_stimulus = stim_data

            # 1. Modulación neuroquímica
            self.neurochemistry.apply_modulation(stim_data["neurochemical_shifts"], intensity=intensity)

            # 2. Activación de nodos específicos
            for nid, weight in stim_data["target_nodes"].items():
                if nid in integrated_node_targets:
                    integrated_node_targets[nid] += weight * intensity

            # 3. Contribución a ondas cerebrales
            for wave, pwr in stim_data["brainwaves"].items():
                integrated_brainwaves[wave] += (pwr - integrated_brainwaves[wave]) * (0.6 * intensity)

            # Narrativa
            active_narratives.append({
                "id": stim_id,
                "name": stim_data["name"],
                "icon": stim_data["icon"],
                "intensity": round(intensity, 2),
                "summary": stim_data["summary"],
                "steps": stim_data["cascade_steps"]
            })

        # Propagación sináptica a través del grafo del conectoma (difusión a nodos vecinos)
        final_activations = {}
        for nid, val in integrated_node_targets.items():
            final_val = max(0.02, min(1.0, val))
            final_activations[nid] = round(final_val, 4)

        # Propagar a nodos corticales cercanos según conectividad del grafo
        for tract in self.connectome.tracts:
            src = tract["src"]
            tgt = tract["tgt"]
            w = tract.get("weight", 0.5)
            if src in final_activations and final_activations[src] > 0.4:
                spread = final_activations[src] * 0.35 * abs(w)
                if tgt in final_activations:
                    final_activations[tgt] = round(min(1.0, max(final_activations[tgt], spread)), 4)

        self.current_activations = final_activations

        # Determinar tractos activos con señal de pulso
        active_tracts_info = []
        for i, tract in enumerate(self.connectome.tracts):
            src_act = final_activations.get(tract["src"], 0.0)
            tgt_act = final_activations.get(tract["tgt"], 0.0)
            combined_activity = (src_act + tgt_act) / 2.0
            if combined_activity > 0.25:
                active_tracts_info.append({
                    "index": i,
                    "src": tract["src"],
                    "tgt": tract["tgt"],
                    "name": tract["name"],
                    "activity": round(combined_activity, 3),
                    "type": tract.get("type", "Standard")
                })

        return {
            "active_stimuli": self.current_active_stimuli,
            "dominant_stimulus": dominant_stimulus["name"] if dominant_stimulus else "Estado Homeostático Basal",
            "dominant_icon": dominant_stimulus["icon"] if dominant_stimulus else "⚖️",
            "dominant_category": dominant_stimulus["category"] if dominant_stimulus else "Homeostasis",
            "narratives": active_narratives,
            "neurochemistry": self.neurochemistry.to_dict(),
            "brainwaves": {k: round(v, 3) for k, v in integrated_brainwaves.items()},
            "node_activations": final_activations,
            "active_tracts": active_tracts_info
        }

    def get_state(self) -> Dict[str, Any]:
        """Obtiene el estado actual sin modificar estímulos."""
        return self.stimulate(self.current_active_stimuli)
