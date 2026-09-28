"""
Lanzador del Servidor del Conectoma Cerebral Humano
Inicia el servidor Flask y muestra la URL local lista para abrir.
"""

import sys
import os
import socket
import webbrowser
from threading import Timer

# Asegurar que el directorio raíz del proyecto esté en sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app import app

def find_available_port(default_port=5000):
    """Encuentra un puerto disponible comenzando por default_port."""
    for port in range(default_port, default_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return default_port

def open_browser(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[!] No se pudo abrir el navegador automáticamente: {e}")

def main():
    port = find_available_port(5000)
    url = f"http://localhost:{port}"

    print("=" * 70)
    print(" 🧠 CONECTOMA DEL CEREBRO HUMANO 3D - SIMULADOR DE REDES NEURONALES")
    print("=" * 70)
    print(f" [*] Estado del Servidor: ONLINE")
    print(f" [*] Abre en tu navegador: {url}")
    print(" [*] Presiona Ctrl+C en la consola para detener el servidor.")
    print("=" * 70)

    # Abrir navegador tras 1.2 segundos
    Timer(1.2, lambda: open_browser(url)).start()

    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
