echo "Ejecutando revisión de estilo con flake8..."
if ! command -v flake8 &> /dev/null
then
    echo "flake8 no está instalado. Instálalo con: pip install flake8"
    exit 1
fi
flake8 gestor.py --max-line-length=100
if [ $? -eq 0 ]; then
    echo "Estilo correcto: flake8 no encontró errores."
else
    echo "Problemas de estilo detectados por flake8."
fi
