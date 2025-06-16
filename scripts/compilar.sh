echo "Verificando errores de sintaxis en gestor.py..."
python -m py_compile gestor.py
if [ $? -eq 0 ]; then
    echo "Código compilado correctamente (sin errores de sintaxis)."
else
    echo "Error de sintaxis detectado en gestor.py"
fi
