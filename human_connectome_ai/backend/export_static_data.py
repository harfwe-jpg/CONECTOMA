"""
Script para generar el JSON precalculado del conectoma y el archivo JS de respaldo.
"""

import json
from backend.connectome_model import BrainConnectome
from backend.stimulus_engine import StimulusEngine

def export_assets():
    connectome = BrainConnectome()
    engine = StimulusEngine(connectome)
    
    connectome_data = connectome.export_data()
    stimuli_catalog = engine.STIMULI_CATALOG
    
    # 1. Guardar data/default_connectome.json
    with open("data/default_connectome.json", "w", encoding="utf-8") as f:
        json.dump({
            "connectome": connectome_data,
            "stimuli": stimuli_catalog
        }, f, indent=2, ensure_ascii=False)
    print("Guardado data/default_connectome.json")

    # 2. Generar frontend/js/fallback_data.js con soporte offline
    fallback_js_content = f"""/**
 * CONNECTOME FALLBACK DATA & CLIENT-SIDE NEURO-ENGINE
 * Permite que la aplicación funcione al 100% de forma autónoma en el navegador
 * o conectada a la API de Python.
 */
window.DEFAULT_CONNECTOME = {json.dumps(connectome_data, ensure_ascii=False)};
window.STIMULI_CATALOG = {json.dumps(stimuli_catalog, ensure_ascii=False)};
"""
    with open("frontend/js/fallback_data.js", "w", encoding="utf-8") as f:
        f.write(fallback_js_content)
    print("Guardado frontend/js/fallback_data.js")

if __name__ == "__main__":
    export_assets()
