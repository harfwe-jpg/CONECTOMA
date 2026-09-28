"""
Servidor API REST y Servidor Web para la Simulación del Conectoma Cerebral Humano 3D.
Construido con Flask y Flask-CORS.
"""

import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

try:
    from backend.connectome_model import BrainConnectome
    from backend.stimulus_engine import StimulusEngine
except ImportError:
    from connectome_model import BrainConnectome
    from stimulus_engine import StimulusEngine

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

# Instanciación del Conectoma y Motor Neuro-computacional
connectome = BrainConnectome()
stimulus_engine = StimulusEngine(connectome)

# ----------------- RUTAS ESTÁTICAS (FRONTEND) -----------------

@app.route("/")
def index():
    """Sirve la interfaz web 3D principal."""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    """Sirve archivos estáticos (CSS, JS, iconos)."""
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/data/<path:path>")
def data_proxy(path):
    """Sirve datos JSON precalculados si se solicitan."""
    return send_from_directory(DATA_DIR, path)

# ----------------- RUTAS API REST (NEUROCIENCIA) -----------------

@app.route("/api/status", methods=["GET"])
def api_status():
    """Estado del motor neurocomputacional."""
    return jsonify({
        "status": "online",
        "engine": "HumanConnectomeSimulationEngine v2.0",
        "nodes_loaded": len(connectome.nodes_data),
        "tracts_loaded": len(connectome.tracts),
        "supported_stimuli": list(stimulus_engine.STIMULI_CATALOG.keys())
    })

@app.route("/api/connectome", methods=["GET"])
def get_connectome():
    """Devuelve la arquitectura estructural 3D del conectoma (nodos y tractografía)."""
    return jsonify(connectome.export_data())

@app.route("/api/stimuli", methods=["GET"])
def get_stimuli():
    """Devuelve el catálogo de estímulos corporales humanos con sus descripciones neurobiológicas."""
    return jsonify(stimulus_engine.STIMULI_CATALOG)

@app.route("/api/stimulate", methods=["POST"])
def post_stimulate():
    """
    Aplica uno o múltiples estímulos con intensidades continuas.
    Payload: {"stimuli": {"hambre": 0.85, "excitacion": 0.70}}
    """
    data = request.get_json(silent=True) or {}
    stimuli = data.get("stimuli", {})
    
    # Si viene formato plano {"hambre": 0.8}
    if not stimuli and any(k in stimulus_engine.STIMULI_CATALOG for k in data.keys()):
        stimuli = data

    result = stimulus_engine.stimulate(stimuli)
    return jsonify(result)

@app.route("/api/state", methods=["GET"])
def get_state():
    """Devuelve el estado dinámico actual del cerebro."""
    return jsonify(stimulus_engine.get_state())

@app.route("/api/reset", methods=["POST"])
def post_reset():
    """Restaura el cerebro al estado homeostático basal."""
    result = stimulus_engine.stimulate({})
    return jsonify(result)

def create_app():
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Servidor Conectoma Cerebral Humano iniciado en: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
