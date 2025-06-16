echo "Ejecutando pruebas con pytest..."
if ! command -v pytest &> /dev/null
then
    echo "pytest no está instalado. Instálalo con: pip install pytest"
    exit 1
fi

pytest --maxfail=1 --disable-warnings -q test/

if [ $? -eq 0 ]; then
    echo "Todas las pruebas pasaron correctamente."
else
    echo "Fallos en las pruebas. Revisa los errores arriba."
fi
