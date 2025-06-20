from flask import Blueprint, render_template, request, jsonify
import json, os
from datetime import datetime

main = Blueprint('main', __name__)
ARCHIVO_JSON = os.path.join(os.path.dirname(__file__), "gastos.json")
gastos = []

def cargar_gastos():
    global gastos
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, 'r') as f:
            contenido = f.read().strip()
            gastos = json.loads(contenido) if contenido else []
    else:
        gastos = []

def guardar_gastos():
    with open(ARCHIVO_JSON, 'w') as f:
        json.dump(gastos, f, indent=4)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/api/gastos', methods=['GET'])
def obtener_gastos():
    categoria = request.args.get("categoria", "Todas")
    mes = request.args.get("mes", "Todas")

    filtrados = []
    for g in gastos:
        cumple_categoria = (categoria == "Todas" or g["categoria"] == categoria)

        try:
            fecha_obj = datetime.strptime(g["fecha"], "%Y-%m-%d %H:%M:%S")
            mes_gasto = fecha_obj.strftime("%m-%Y")
        except Exception:
            mes_gasto = "Sin fecha"

        cumple_mes = (mes == "Todas" or mes_gasto == mes)

        if cumple_categoria and cumple_mes:
            filtrados.append(g)

    return jsonify(filtrados)

@main.route('/api/gastos', methods=['POST'])
def agregar_gasto():
    data = request.json
    gasto = {
        "categoria": data['categoria'],
        "subcategoria": data['subcategoria'],
        "monto": float(data['monto']),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    gastos.append(gasto)
    guardar_gastos()
    return jsonify({"mensaje": "Gasto agregado"}), 201

@main.route('/api/gastos/<int:idx>', methods=['DELETE'])
def eliminar_gasto(idx):
    try:
        gastos.pop(idx)
        guardar_gastos()
        return jsonify({"mensaje": "Eliminado"}), 200
    except IndexError:
        return jsonify({"error": "Índice no válido"}), 404

@main.route('/api/meses', methods=['GET'])
def obtener_meses():
    desde = datetime(2025, 1, 1)
    hoy = datetime.now()
    meses = []

    while desde <= hoy:
        meses.append(desde.strftime("%m-%Y"))
        if desde.month == 12:
            desde = datetime(desde.year + 1, 1, 1)
        else:
            desde = datetime(desde.year, desde.month + 1, 1)

    return jsonify(["Todas"] + meses)

# Cargar al arrancar
cargar_gastos()
