# 🧠 Simulador del Conectoma del Cerebro Humano 3D & Redes de Estímulos

Un simulador neurocomputacional e interactivo en 3D que modela las vías del **conectoma cerebral humano**, la propagación de potenciales de acción a través de haces de sustancia blanca (tractografía axonal), las oscilaciones de ondas cerebrales (EEG) y las cascadas neuroendocrinas ante estímulos corporales vitales (como el **hambre**, la **excitación sexual**, el **miedo**, el **dolor agudo**, el **enfoque ejecutivo** y el **sueño profundo**).

---

## 🔬 Arquitectura Neurobiológica del Conectoma

El sistema modela tanto núcleos anatómicos corticales como subcorticales en coordenadas 3D estandarizadas (espacio MNI), integrando sus interconexiones de tractografía:

### 1. ¿Cómo actúa el cerebro ante el Hambre y el Apetito Metabólico? (`hambre`)
- **Fase 1 (Aferencia Periférica):** El descenso de glucosa y contracciones gástricas inducen la secreción de **Grelina**. La señal asciende por el **Nervio Vago** hasta el **Núcleo del Tracto Solitario (NTS)** en el tronco encefálico.
- **Fase 2 (Centro del Hambre):** El NTS activa masivamente las neuronas orexinérgicas y de Neuropéptido Y (NPY) en el **Hipotálamo Lateral (HYPO_LH)**, mientras se inhibe el centro de saciedad (**Hipotálamo Ventromedial**).
- **Fase 3 (Conciencia Interoceptiva):** La **Corteza Insular (Ínsula)** decodifica la sensación somática visceral de vacío gástrico.
- **Fase 4 (Urgencia de Recompensa - "Wanting"):** El **Área Tegmental Ventral (VTA)** vierte dopamina en el **Núcleo Accumbens (NAcc)**, generando una motivación imperiosa de buscar comida calórica.
- **Fase 5 (Toma de Decisiones):** La **Corteza Orbitofrontal (OFC)** simula aromas y texturas, dirigiendo a la **Corteza Prefrontal Dorsolateral (DLPFC)** a planificar la acción motora de alimentación.

### 2. ¿Cómo actúa el cerebro ante la Excitación Sexual, Deseo y Clímax? (`excitacion`)
- **Fase 1 (Gatillo Sensorial):** Estímulos táctiles de zonas erógenas (procesados en la **Corteza Somatosensorial S1**), imágenes (en **V1**) o pensamientos activan la **Amígdala** y el sistema límbico.
- **Fase 2 (Ignición Hipotalámica):** Despolarización máxima en el **Área Preóptica Medial (HYPO_MPOA)**, switch biológico central del impulso y conducta copulatoria.
- **Fase 3 (Torrente Mesolímbico de Placer):** El MPOA dispara al **VTA**, desencadenando una inundación de **Dopamina** en el **Núcleo Accumbens**.
- **Fase 4 (Hipofrontalidad Transitoria):** Se atenúa el control inhibitorio de la **Corteza Prefrontal Dorsolateral (DLPFC)**. Esto reduce la timidez, el miedo al juicio social y el pudor, permitiendo entregarse a la experiencia sensorial.
- **Fase 5 (Orgasmo y Vínculo):** El **Núcleo Paraventricular (HYPO_PVN)** libera oleadas masivas de **Oxitocina** y **Endorfinas endógenas**, generando analgesia, euforia y relajación post-orgásmica.

### 3. Otros Estímulos y Redes Implementadas:
- **Miedo / Pánico (`miedo`):** Vía rápida talámica de 12 ms a la Amígdala -> Locus Coeruleus (Noradrenalina) -> Eje HPA (Cortisol) -> Tono motor (M1) de lucha o escape.
- **Dolor Agudo (`dolor`):** Haz espinotalámico -> Tálamo (VPL) -> S1 (localización espacial) -> Cíngulo Anterior ACC (sufrimiento subjetivo) -> Ínsula visceral.
- **Enfoque / Flow (`enfoque`):** Red fronto-parietal activa (DLPFC + ACC), supresión de la red por defecto (DMN), dopamina tónica equilibrada.
- **Sueño Profundo (`sueno`):** Acumulación de adenosina -> Núcleo Preóptico Ventrolateral (VLPO) libera GABA -> inhibición de centros de vigilia -> Melatonina pineal -> ondas Delta lentas.
- **Amor y Apego (`amor`):** Oxitocina en Núcleo Accumbens e Ínsula, desactivación del recelo social de la amígdala.
- **Euforia y Logro (`euforia`):** Máxima descarga VTA-Accumbens con endorfinas y dopamina al 100%.

---

## 🛠️ Tecnologías Empleadas

- **Python (Flask, NetworkX, NumPy):** Motor neuro-computacional backend que modela el grafo del conectoma, ecuaciones de propagación sináptica y niveles de 10 neurotransmisores en tiempo real.
- **Three.js (WebGL):** Visualización 3D interactiva del encéfalo, núcleos anatómicos con sombreadores emisivos, nubes de partículas corticales y tractografía axonal con splines Catmull-Rom.
- **HTML5 & CSS3:** Interfaz Cyber-Neuro translúcida (Glassmorphism), paneles HUD, oscilograma EEG y diseño responsive de alta precisión.
- **Web Audio API:** Síntesis sonora bioacústica con clics de disparo de potenciales de acción y oscilador binaural sincronizado al arousal cerebral.

---

## 🚀 Cómo Ejecutar la Aplicación

### Opción 1: Con Backend Python Completo (Recomendado)
Ejecuta el archivo `run.bat` o desde la terminal PowerShell:
```bash
python backend/run_server.py
```
El servidor detectará un puerto libre (por defecto `http://localhost:5000`) y abrirá automáticamente tu navegador web.

### Opción 2: Modo Autónomo en Navegador Directo
Simplemente abre `frontend/index.html` en cualquier navegador web moderno (Chrome, Edge, Firefox, Brave, Safari). La aplicación detectará automáticamente el entorno y activará el **motor neurocomputacional de respaldo en JavaScript** para funcionar al 100% sin dependencias externas.

---

## 🎮 Controles de Interacción 3D

- **Rotación:** Click izquierdo + arrastrar en el lienzo 3D.
- **Zoom:** Rueda del mouse (scroll).
- **Paneo:** Click derecho + arrastrar.
- **Inspección de Núcleos:** Pasa el cursor (hover) o haz clic en cualquier esfera coloreada para ver sus coordenadas MNI, neurotransmisores asociados y su función fisiológica en el panel derecho.
- **Presets de Cámara:** Botones inferiores para alternar entre perspectiva 3D, corte sagital (lateral), coronal (frontal) o axial (superior).
- **Capas de Visualización:** Botones inferiores para aislar el subcórtex, visualizar solo los haces de tractografía, o ver el cerebro completo.
