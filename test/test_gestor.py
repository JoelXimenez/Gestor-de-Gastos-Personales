import sys
import os
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gestor import GestorGastosApp


def test_guardar_y_cargar():
    app = GestorGastosApp()
    app.gastos = []

    gasto = {
        "categoria": "Universidad",
        "subcategoria": "Prueba",
        "monto": 20.0,
        "fecha": "2025-06-16 15:30:00"
    }

    app.gastos.append(gasto)
    app.archivo_json = "gastos_test.json"  
    app.guardar_gastos()

    assert os.path.exists("gastos_test.json")

    with open("gastos_test.json", "r") as f:
        data = json.load(f)
        assert isinstance(data, list)
        assert data[-1]["categoria"] == "Universidad"
        assert data[-1]["monto"] == 20.0

    os.remove("gastos_test.json")
