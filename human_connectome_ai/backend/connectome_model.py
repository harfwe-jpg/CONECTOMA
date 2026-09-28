"""
Módulo del Conectoma Estructural del Cerebro Humano
Modela nodos anatómicos (corticales y subcorticales), coordenadas MNI normalizadas,
haces de sustancia blanca (tractografía axonal) y grafos de conectividad con NetworkX.
"""

import math
import random
from typing import Dict, List, Any
import networkx as nx

class BrainConnectome:
    """Representa el grafo del conectoma humano con núcleos anatómicos y tractografía."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes_data: Dict[str, Dict[str, Any]] = {}
        self.tracts: List[Dict[str, Any]] = []
        self._build_anatomical_nuclei()
        self._build_cortical_mantle()
        self._build_white_matter_tracts()

    def _build_anatomical_nuclei(self):
        """Define los núcleos neuroanatómicos clave con coordenadas 3D estandarizadas."""
        # Coordenadas orientadas en espacio 3D (X: Izquierda/Derecha, Y: Posterior/Anterior, Z: Inferior/Superior)
        nuclei = [
            # --- HIPOTÁLAMO Y TRONCO (Centro homeostático, hambre, sexo, vigilia) ---
            {
                "id": "HYPO_LH", "name": "Hipotálamo Lateral", "group": "Limbic",
                "pos": [0.0, 3.5, -4.0], "radius": 2.2, "color": "#F59E0B",
                "desc": "Centro del hambre, impulsado por Orexina y Neuropéptido Y. Despierta la búsqueda activa de alimento y alerta metabólica.",
                "transmitters": ["ghrelin", "dopamine", "norepinephrine"]
            },
            {
                "id": "HYPO_VMH", "name": "Hipotálamo Ventromedial", "group": "Limbic",
                "pos": [0.0, 2.0, -5.5], "radius": 2.0, "color": "#10B981",
                "desc": "Centro de la saciedad y plenitud gástrica mediada por leptina y serotonina.",
                "transmitters": ["serotonin", "gaba"]
            },
            {
                "id": "HYPO_MPOA", "name": "Área Preóptica Medial (MPOA)", "group": "Limbic",
                "pos": [0.0, 6.0, -3.0], "radius": 2.3, "color": "#F43F5E",
                "desc": "Epicentro de la motivación y apetito sexual (libido), conducta copulatoria y termorregulación.",
                "transmitters": ["dopamine", "oxytocin", "endorphins"]
            },
            {
                "id": "HYPO_PVN", "name": "Núcleo Paraventricular", "group": "Limbic",
                "pos": [0.0, 4.0, -2.0], "radius": 2.0, "color": "#EF4444",
                "desc": "Eje HPA del estrés (secreción de CRH -> Cortisol) y síntesis neuroendocrina de Oxitocina y Vasopresina.",
                "transmitters": ["cortisol", "oxytocin", "norepinephrine"]
            },

            # --- VTA Y SISTEMA DE RECOMPENSA MESOLÍMBICO ---
            {
                "id": "VTA", "name": "Área Tegmental Ventral (VTA)", "group": "Subcortical",
                "pos": [0.0, -8.0, -7.5], "radius": 2.4, "color": "#FBBF24",
                "desc": "Fábrica primaria de Dopamina. Se enciende explosivamente ante deseo sexual, anticipación de comida y drogas.",
                "transmitters": ["dopamine"]
            },
            {
                "id": "NACC_L", "name": "Núcleo Accumbens (Izq)", "group": "Subcortical",
                "pos": [-6.0, 7.0, -4.5], "radius": 2.5, "color": "#F59E0B",
                "desc": "Hub del placer, 'wanting' (deseo imperioso) y valor hedónico. Crucial en adicciones y orgasmo.",
                "transmitters": ["dopamine", "endorphins", "gaba"]
            },
            {
                "id": "NACC_R", "name": "Núcleo Accumbens (Der)", "group": "Subcortical",
                "pos": [6.0, 7.0, -4.5], "radius": 2.5, "color": "#F59E0B",
                "desc": "Hub del placer y deseo bilateral; integra refuerzo positivo y anticipación de placer.",
                "transmitters": ["dopamine", "endorphins", "gaba"]
            },

            # --- AMÍGDALAS (Alarma, miedo, excitación emocional) ---
            {
                "id": "AMYG_L", "name": "Amígdala Basolateral (Izq)", "group": "Limbic",
                "pos": [-14.0, 1.0, -10.0], "radius": 2.6, "color": "#DC2626",
                "desc": "Detector de amenaza biológica, pánico y condicionamiento del miedo. Reacciona en 12 milisegundos.",
                "transmitters": ["norepinephrine", "glutamate", "cortisol"]
            },
            {
                "id": "AMYG_R", "name": "Amígdala Basolateral (Der)", "group": "Limbic",
                "pos": [14.0, 1.0, -10.0], "radius": 2.6, "color": "#DC2626",
                "desc": "Evaluación afectiva, modulación de excitación sexual y activación simpática bilateral.",
                "transmitters": ["norepinephrine", "glutamate", "cortisol"]
            },

            # --- HIPOCAMPO (Memoria episódica y mapa espacial) ---
            {
                "id": "HIPP_L", "name": "Hipocampo (Izq)", "group": "Limbic",
                "pos": [-16.0, -14.0, -7.0], "radius": 2.6, "color": "#3B82F6",
                "desc": "Consolidación de recuerdos a largo plazo y evocación contextual de experiencias pasadas.",
                "transmitters": ["glutamate", "serotonin"]
            },
            {
                "id": "HIPP_R", "name": "Hipocampo (Der)", "group": "Limbic",
                "pos": [16.0, -14.0, -7.0], "radius": 2.6, "color": "#3B82F6",
                "desc": "Navegación espacial y memoria afectiva de recompensas y lugares seguros.",
                "transmitters": ["glutamate", "serotonin"]
            },

            # --- ÍNSULA (Interocepción, vísceras, dolor visceral, sensaciones eróticas) ---
            {
                "id": "INSULA_L", "name": "Corteza Insular Anterior (Izq)", "group": "Cortical",
                "pos": [-20.0, 6.0, 1.0], "radius": 2.7, "color": "#EA580C",
                "desc": "Conciencia somática e interoceptiva: detecta el rugido gástrico de hambre, dolor visceral y calidez íntima.",
                "transmitters": ["glutamate", "serotonin"]
            },
            {
                "id": "INSULA_R", "name": "Corteza Insular Anterior (Der)", "group": "Cortical",
                "pos": [20.0, 6.0, 1.0], "radius": 2.7, "color": "#EA580C",
                "desc": "Integración autonómica, ritmo cardíaco acelerado durante la excitación y empatía visceral.",
                "transmitters": ["glutamate", "norepinephrine"]
            },

            # --- TÁLAMO (Relé y filtro sensorial central) ---
            {
                "id": "THAL_L", "name": "Tálamo Pulvinar / VPL (Izq)", "group": "Subcortical",
                "pos": [-7.0, -9.0, 2.0], "radius": 2.8, "color": "#8B5CF6",
                "desc": "Estación central de relevo que proyecta señales de dolor, tacto y visión hacia la corteza.",
                "transmitters": ["glutamate", "gaba"]
            },
            {
                "id": "THAL_R", "name": "Tálamo Pulvinar / VPL (Der)", "group": "Subcortical",
                "pos": [7.0, -9.0, 2.0], "radius": 2.8, "color": "#8B5CF6",
                "desc": "Puerta de entrada talámica para los estímulos ascendentes del cuerpo y la médula espinal.",
                "transmitters": ["glutamate", "gaba"]
            },

            # --- CORTEZA CINGULADA ANTERIOR (ACC) ---
            {
                "id": "ACC", "name": "Corteza Cingulada Anterior (ACC)", "group": "Limbic",
                "pos": [0.0, 15.0, 12.0], "radius": 2.8, "color": "#E11D48",
                "desc": "Procesamiento del dolor afectivo/sufrimiento, resolución de conflicto emocional y esfuerzo de voluntad.",
                "transmitters": ["glutamate", "dopamine", "endorphins"]
            },

            # --- CORTEZA PREFRONTAL DORSOLATERAL (DLPFC - Razón, control ejecutivo) ---
            {
                "id": "DLPFC_L", "name": "Corteza Prefrontal Dorsolateral (Izq)", "group": "Cortical",
                "pos": [-24.0, 28.0, 16.0], "radius": 3.0, "color": "#06B6D4",
                "desc": "Freno racional, memoria de trabajo y planificación. Se desactiva durante el orgasmo y el pánico extremo.",
                "transmitters": ["dopamine", "norepinephrine", "glutamate"]
            },
            {
                "id": "DLPFC_R", "name": "Corteza Prefrontal Dorsolateral (Der)", "group": "Cortical",
                "pos": [24.0, 28.0, 16.0], "radius": 3.0, "color": "#06B6D4",
                "desc": "Toma de decisiones estratégica, autocontrol inhibitorio frente a impulsos primarios.",
                "transmitters": ["dopamine", "norepinephrine", "glutamate"]
            },

            # --- CORTEZA ORBITOFRONTAL (OFC - Valor hedónico y recompensa) ---
            {
                "id": "OFC_L", "name": "Corteza Orbitofrontal (Izq)", "group": "Cortical",
                "pos": [-12.0, 26.0, -6.0], "radius": 2.8, "color": "#14B8A6",
                "desc": "Asigna valor hedónico subjetivo a la comida, parejas sexuales y dinero. Evalúa '¿vale la pena el esfuerzo?'.",
                "transmitters": ["dopamine", "serotonin"]
            },
            {
                "id": "OFC_R", "name": "Corteza Orbitofrontal (Der)", "group": "Cortical",
                "pos": [12.0, 26.0, -6.0], "radius": 2.8, "color": "#14B8A6",
                "desc": "Evaluación gustativa y erótica sensorial; calcula el balance costo-beneficio del impulso biológico.",
                "transmitters": ["dopamine", "serotonin"]
            },

            # --- CORTEZA SOMATOSENSORIAL PRIMARIA (S1 - Tacto, zonas erógenas, dolor) ---
            {
                "id": "S1_L", "name": "Corteza Somatosensorial (Izq)", "group": "Cortical",
                "pos": [-26.0, -12.0, 25.0], "radius": 2.9, "color": "#EC4899",
                "desc": "Homúnculo somatosensorial: mapa táctil del cuerpo, dolor agudo, caricias y zonas erógenas.",
                "transmitters": ["glutamate"]
            },
            {
                "id": "S1_R", "name": "Corteza Somatosensorial (Der)", "group": "Cortical",
                "pos": [26.0, -12.0, 25.0], "radius": 2.9, "color": "#EC4899",
                "desc": "Procesamiento táctil contralateral y mapeo de intensidad sensorial física.",
                "transmitters": ["glutamate"]
            },

            # --- CORTEZA MOTORA PRIMARIA (M1 - Acción motriz, huida, aproximación) ---
            {
                "id": "M1_L", "name": "Corteza Motora Primaria (Izq)", "group": "Cortical",
                "pos": [-24.0, 0.0, 28.0], "radius": 2.9, "color": "#6366F1",
                "desc": "Comando voluntario de músculos para cazar comida, acercarse en cortejo íntimo o correr ante peligro.",
                "transmitters": ["glutamate", "dopamine"]
            },
            {
                "id": "M1_R", "name": "Corteza Motora Primaria (Der)", "group": "Cortical",
                "pos": [24.0, 0.0, 28.0], "radius": 2.9, "color": "#6366F1",
                "desc": "Control motor contralateral e inicio del movimiento fisiológico coordinado.",
                "transmitters": ["glutamate", "dopamine"]
            },

            # --- CORTEZA VISUAL PRIMARIA (V1 - Estímulos visuales eróticos o de presa/depredador) ---
            {
                "id": "V1", "name": "Corteza Visual Primaria (V1 Calcarina)", "group": "Cortical",
                "pos": [0.0, -42.0, 4.0], "radius": 3.0, "color": "#84CC16",
                "desc": "Entrada óptica: decodifica rostros atractivos, señales sexuales visuales, alimento o sombras amenazantes.",
                "transmitters": ["glutamate"]
            },

            # --- TRONCO ENCEFÁLICO Y CENTROS VITALES ---
            {
                "id": "LOCUS_COERULEUS", "name": "Locus Coeruleus", "group": "Brainstem",
                "pos": [0.0, -22.0, -14.0], "radius": 2.2, "color": "#EF4444",
                "desc": "Torrente de Noradrenalina. Dispara la taquicardia, dilatación pupilar y estado de máxima alarma.",
                "transmitters": ["norepinephrine"]
            },
            {
                "id": "RAPHE_NUCLEI", "name": "Núcleos del Rafe", "group": "Brainstem",
                "pos": [0.0, -20.0, -12.0], "radius": 2.1, "color": "#10B981",
                "desc": "Polo productor de Serotonina que baña todo el cerebro para amortiguar el impulso y generar templanza.",
                "transmitters": ["serotonin"]
            },
            {
                "id": "NTS_SOLITARY", "name": "Núcleo del Tracto Solitario", "group": "Brainstem",
                "pos": [0.0, -26.0, -20.0], "radius": 2.0, "color": "#EAB308",
                "desc": "Receptor del Nervio Vago: comunica el estado del estómago vacío/lleno y la presión arterial al cerebro.",
                "transmitters": ["ghrelin", "glutamate"]
            },
            {
                "id": "VLPO", "name": "Núcleo Preóptico Ventrolateral", "group": "Limbic",
                "pos": [0.0, 8.0, -5.0], "radius": 2.1, "color": "#3B82F6",
                "desc": "Interruptor maestro del sueño. Libera GABA para 'apagar' los centros de vigilia y descansar.",
                "transmitters": ["gaba"]
            },
            {
                "id": "PINEAL", "name": "Glándula Pineal", "group": "Subcortical",
                "pos": [0.0, -20.0, 0.0], "radius": 1.8, "color": "#6366F1",
                "desc": "Transductor neuroendocrino que vierte Melatonina ante la oscuridad nocturna.",
                "transmitters": ["melatonin"]
            },

            # --- CEREBELO (Coordinación y balance motor/afectivo) ---
            {
                "id": "CEREBELLUM_L", "name": "Hemisferio Cerebeloso (Izq)", "group": "Cerebellum",
                "pos": [-20.0, -32.0, -18.0], "radius": 3.2, "color": "#A855F7",
                "desc": "Refinamiento micrométrico de la acción motriz, sincronización temporal y equilibrio.",
                "transmitters": ["gaba", "glutamate"]
            },
            {
                "id": "CEREBELLUM_R", "name": "Hemisferio Cerebeloso (Der)", "group": "Cerebellum",
                "pos": [20.0, -32.0, -18.0], "radius": 3.2, "color": "#A855F7",
                "desc": "Automatización procedural y calibración sensorial de movimientos físicos rápidos.",
                "transmitters": ["gaba", "glutamate"]
            }
        ]

        for n in nuclei:
            self.nodes_data[n["id"]] = n
            self.graph.add_node(n["id"], **n)

    def _build_cortical_mantle(self):
        """Genera una distribución orgánica de nodos corticales sobre la superficie del encéfalo."""
        random.seed(42)  # Semilla determinista para reproducibilidad de la forma anatómica
        
        # Parámetros del elipsoide cortical humano
        a = 34.0  # Ancho medio (eje X, lateral)
        b = 46.0  # Largo medio (eje Y, antero-posterior)
        c = 32.0  # Alto medio (eje Z, dorso-ventral)

        cortical_regions = [
            {"lobe": "Frontal", "y_range": (10, 44), "z_range": (-5, 30), "color": "#38BDF8"},
            {"lobe": "Parietal", "y_range": (-25, 12), "z_range": (14, 34), "color": "#F472B6"},
            {"lobe": "Occipital", "y_range": (-46, -22), "z_range": (-8, 18), "color": "#A3E635"},
            {"lobe": "Temporal", "y_range": (-28, 16), "z_range": (-22, 6), "color": "#FB923C"}
        ]

        node_count = 0
        target_mantle_nodes = 320

        while node_count < target_mantle_nodes:
            # Coordenadas esféricas con perturbación giro-sulcal
            u = random.uniform(0, math.pi * 2)
            v = random.uniform(0.15, math.pi - 0.15)
            
            # Deformación sulcal / fisura interhemisférica
            sin_v = math.sin(v)
            cos_v = math.cos(v)
            sin_u = math.sin(u)
            cos_u = math.cos(u)

            x = a * sin_v * cos_u
            y = b * sin_v * sin_u
            z = c * cos_v

            # Crear surco interhemisférico (hendidura central en X=0)
            if abs(x) < 4.0 and z > 5.0:
                continue

            # Ondulación giros / circunvoluciones cerebrales
            sulcal_wave = 1.0 + 0.08 * math.sin(x * 0.4) * math.cos(y * 0.3) * math.sin(z * 0.5)
            x *= sulcal_wave
            y *= sulcal_wave
            z *= sulcal_wave

            # Clasificar en lóbulo
            assigned_lobe = "Frontal"
            assigned_color = "#38BDF8"
            for cr in cortical_regions:
                if cr["y_range"][0] <= y <= cr["y_range"][1] and cr["z_range"][0] <= z <= cr["z_range"][1]:
                    assigned_lobe = cr["lobe"]
                    assigned_color = cr["color"]
                    break

            node_id = f"CORTEX_{assigned_lobe[:3].upper()}_{node_count:03d}"
            cortex_node = {
                "id": node_id,
                "name": f"Neurona Cortical ({assigned_lobe})",
                "group": "CortexMantle",
                "lobe": assigned_lobe,
                "pos": [round(x, 2), round(y, 2), round(z, 2)],
                "radius": 1.1,
                "color": assigned_color,
                "desc": f"Red sináptica de la corteza cerebral en el lóbulo {assigned_lobe}.",
                "transmitters": ["glutamate", "gaba"]
            }

            self.nodes_data[node_id] = cortex_node
            self.graph.add_node(node_id, **cortex_node)
            node_count += 1

    def _build_white_matter_tracts(self):
        """Conecta núcleos anatómicos y corteza mediante tractos axónicos realistas."""
        # Tractos principales biológicos documentados en tractografía de tensor de difusión (DTI)
        major_tracts = [
            # Haz Prosencefálico Medial (MFB) - Superautopista de la Recompensa y Deseo
            {"src": "VTA", "tgt": "NACC_L", "name": "Vía Mesolímbica Dopaminérgica (Izq)", "weight": 0.95, "type": "Reward"},
            {"src": "VTA", "tgt": "NACC_R", "name": "Vía Mesolímbica Dopaminérgica (Der)", "weight": 0.95, "type": "Reward"},
            {"src": "VTA", "tgt": "HYPO_MPOA", "name": "Tracto VTA-MPOA (Deseo Copulatorio)", "weight": 0.90, "type": "Sexual"},
            {"src": "VTA", "tgt": "AMYG_L", "name": "Vía Mesolímbica Amigdalina", "weight": 0.85, "type": "Arousal"},
            {"src": "VTA", "tgt": "OFC_L", "name": "Vía Mesocortical Prefrontal", "weight": 0.88, "type": "RewardValuation"},
            {"src": "VTA", "tgt": "OFC_R", "name": "Vía Mesocortical Prefrontal", "weight": 0.88, "type": "RewardValuation"},
            
            # Eje del Apetito / Hambre (Intestino -> Vago -> Hipotálamo -> Recompensa)
            {"src": "NTS_SOLITARY", "tgt": "HYPO_LH", "name": "Vía Vagal Ascendente de Hambre", "weight": 0.95, "type": "Hunger"},
            {"src": "NTS_SOLITARY", "tgt": "INSULA_L", "name": "Vía Visceral Gustativa-Gástrica", "weight": 0.90, "type": "Hunger"},
            {"src": "HYPO_LH", "tgt": "NACC_L", "name": "Tracto Orexinérgico Apetitivo", "weight": 0.92, "type": "Hunger"},
            {"src": "HYPO_LH", "tgt": "NACC_R", "name": "Tracto Orexinérgico Apetitivo", "weight": 0.92, "type": "Hunger"},
            {"src": "HYPO_LH", "tgt": "OFC_L", "name": "Eje Hipotalámico-Orbitofrontal", "weight": 0.85, "type": "Hunger"},
            {"src": "INSULA_L", "tgt": "ACC", "name": "Proyección Ínsula-Cíngulo Interoceptivo", "weight": 0.88, "type": "Interoception"},
            {"src": "INSULA_R", "tgt": "ACC", "name": "Proyección Ínsula-Cíngulo Interoceptivo", "weight": 0.88, "type": "Interoception"},
            {"src": "OFC_L", "tgt": "DLPFC_L", "name": "Integración Decisoria de Búsqueda de Alimento", "weight": 0.82, "type": "Executive"},

            # Circuito de la Excitación Sexual y Placer (MPOA -> VTA -> NAcc -> Oxitocina)
            {"src": "HYPO_MPOA", "tgt": "VTA", "name": "Eje Hipotalámico-Tegmental Sexual", "weight": 0.98, "type": "Sexual"},
            {"src": "HYPO_MPOA", "tgt": "HYPO_PVN", "name": "Señalización de Oxitocina Erótica", "weight": 0.92, "type": "Sexual"},
            {"src": "NACC_L", "tgt": "OFC_L", "name": "Retroalimentación Hedónica Estriatal", "weight": 0.90, "type": "Sexual"},
            {"src": "NACC_R", "tgt": "OFC_R", "name": "Retroalimentación Hedónica Estriatal", "weight": 0.90, "type": "Sexual"},
            {"src": "S1_L", "tgt": "INSULA_L", "name": "Aferencia Táctil Genital/Sensorial a Ínsula", "weight": 0.92, "type": "Sexual"},
            {"src": "S1_R", "tgt": "INSULA_R", "name": "Aferencia Táctil Genital/Sensorial a Ínsula", "weight": 0.92, "type": "Sexual"},
            {"src": "V1", "tgt": "AMYG_L", "name": "Vía Visual Dorsal Erótica/Amígdala", "weight": 0.86, "type": "Sensory"},
            {"src": "V1", "tgt": "AMYG_R", "name": "Vía Visual Dorsal Erótica/Amígdala", "weight": 0.86, "type": "Sensory"},
            {"src": "DLPFC_L", "tgt": "HYPO_MPOA", "name": "Inhibición Prefrontal de Impulso (Freno)", "weight": -0.75, "type": "Inhibitory"},

            # Circuito del Miedo y Alarma (Amígdala -> Locus Coeruleus -> Motor)
            {"src": "THAL_L", "tgt": "AMYG_L", "name": "Vía Rápida Subcortical de Miedo (12ms)", "weight": 0.98, "type": "Fear"},
            {"src": "THAL_R", "tgt": "AMYG_R", "name": "Vía Rápida Subcortical de Miedo (12ms)", "weight": 0.98, "type": "Fear"},
            {"src": "AMYG_L", "tgt": "LOCUS_COERULEUS", "name": "Tracto Amígdalo-Coerúleo Noradrenérgico", "weight": 0.96, "type": "Fear"},
            {"src": "AMYG_R", "tgt": "LOCUS_COERULEUS", "name": "Tracto Amígdalo-Coerúleo Noradrenérgico", "weight": 0.96, "type": "Fear"},
            {"src": "AMYG_L", "tgt": "HYPO_PVN", "name": "Activación Eje Cortisol HPA", "weight": 0.94, "type": "Fear"},
            {"src": "LOCUS_COERULEUS", "tgt": "M1_L", "name": "Arousal Noradrenérgico Motor (Lucha/Huida)", "weight": 0.90, "type": "Motor"},
            {"src": "LOCUS_COERULEUS", "tgt": "M1_R", "name": "Arousal Noradrenérgico Motor (Lucha/Huida)", "weight": 0.90, "type": "Motor"},

            # Circuito del Dolor Agudo (Espinotalámico -> Tálamo -> S1 -> ACC)
            {"src": "THAL_L", "tgt": "S1_L", "name": "Radiación Espinotalámica Somatosensorial (Ubicación Dolor)", "weight": 0.95, "type": "Pain"},
            {"src": "THAL_R", "tgt": "S1_R", "name": "Radiación Espinotalámica Somatosensorial (Ubicación Dolor)", "weight": 0.95, "type": "Pain"},
            {"src": "THAL_L", "tgt": "ACC", "name": "Tracto Tálamo-Cingulado (Sufrimiento Afectivo del Dolor)", "weight": 0.96, "type": "Pain"},
            {"src": "ACC", "tgt": "INSULA_L", "name": "Integración Dolor Visceral y Emocional", "weight": 0.92, "type": "Pain"},
            {"src": "ACC", "tgt": "AMYG_L", "name": "Alerta de Angustia por Daño Tisular", "weight": 0.88, "type": "Pain"},

            # Circuito del Sueño e Inhibición (VLPO -> Apagado de centros de vigilia)
            {"src": "VLPO", "tgt": "LOCUS_COERULEUS", "name": "Inhibición GABAérgica de Alerta", "weight": -0.95, "type": "SleepInhibition"},
            {"src": "VLPO", "tgt": "VTA", "name": "Inhibición GABAérgica de Recompensa/Vigilia", "weight": -0.90, "type": "SleepInhibition"},
            {"src": "VLPO", "tgt": "HYPO_LH", "name": "Supresión de Orexina (Apetito e Insomnio)", "weight": -0.92, "type": "SleepInhibition"},
            {"src": "PINEAL", "tgt": "VLPO", "name": "Disparo Melatoninérgico de Inducción de Sueño", "weight": 0.92, "type": "Sleep"},

            # Circuito de Enfoque y Control Ejecutivo (Frontoparietal Attention Network)
            {"src": "DLPFC_L", "tgt": "ACC", "name": "Control Atencional Ejecutivo", "weight": 0.90, "type": "Cognitive"},
            {"src": "DLPFC_R", "tgt": "ACC", "name": "Control Atencional Ejecutivo", "weight": 0.90, "type": "Cognitive"},
            {"src": "DLPFC_L", "tgt": "M1_L", "name": "Comando Motor Voluntario Planificado", "weight": 0.85, "type": "Cognitive"},
            {"src": "CEREBELLUM_L", "tgt": "THAL_R", "name": "Circuito Córtico-Ponto-Cerebeloso", "weight": 0.86, "type": "Motor"}
        ]

        for t in major_tracts:
            if t["src"] in self.nodes_data and t["tgt"] in self.nodes_data:
                self.tracts.append(t)
                self.graph.add_edge(t["src"], t["tgt"], **t)

        # Generar tractos axónicos de conexión con la corteza circundante (radiaciones y comisuras)
        cortical_nodes = [nid for nid in self.nodes_data if nid.startswith("CORTEX_")]
        
        # Conectar tálamo con nodos corticales sensoriales y prefrontales
        for cn_id in cortical_nodes[:90]:
            cn = self.nodes_data[cn_id]
            is_left = cn["pos"][0] < 0
            hub = "THAL_L" if is_left else "THAL_R"
            dist = math.dist(cn["pos"], self.nodes_data[hub]["pos"])
            if dist < 42.0:
                tract_item = {
                    "src": hub,
                    "tgt": cn_id,
                    "name": f"Radiación Tálamo-Cortical ({cn['lobe']})",
                    "weight": round(0.4 + 0.3 * (1.0 - dist / 42.0), 3),
                    "type": "Thalamocortical"
                }
                self.tracts.append(tract_item)
                self.graph.add_edge(hub, cn_id, **tract_item)

        # Conectar el Cuerpo Calloso (comisuras interhemisféricas entre nodos cercanos simétricos)
        left_cortex = [nid for nid in cortical_nodes if self.nodes_data[nid]["pos"][0] < -5.0][:50]
        right_cortex = [nid for nid in cortical_nodes if self.nodes_data[nid]["pos"][0] > 5.0][:50]

        for l_id in left_cortex:
            l_pos = self.nodes_data[l_id]["pos"]
            for r_id in right_cortex:
                r_pos = self.nodes_data[r_id]["pos"]
                # Similitud en Y y Z
                dy = abs(l_pos[1] - r_pos[1])
                dz = abs(l_pos[2] - r_pos[2])
                if dy < 8.0 and dz < 8.0:
                    tract_item = {
                        "src": l_id,
                        "tgt": r_id,
                        "name": "Fibra del Cuerpo Calloso (Interhemisférica)",
                        "weight": 0.65,
                        "type": "CorpusCallosum"
                    }
                    self.tracts.append(tract_item)
                    self.graph.add_edge(l_id, r_id, **tract_item)
                    break

    def export_data(self) -> Dict[str, Any]:
        """Exporta la estructura completa lista para ser consumida por Three.js."""
        return {
            "nodes": list(self.nodes_data.values()),
            "tracts": self.tracts,
            "metrics": {
                "total_nodes": len(self.nodes_data),
                "total_tracts": len(self.tracts),
                "anatomical_nuclei": len([n for n in self.nodes_data.values() if not n["id"].startswith("CORTEX_")]),
                "cortical_mantle_nodes": len([n for n in self.nodes_data.values() if n["id"].startswith("CORTEX_")])
            }
        }
