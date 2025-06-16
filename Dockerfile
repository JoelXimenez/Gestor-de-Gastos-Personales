# Imagen base estable
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar CustomTkinter
RUN pip install customtkinter

# Ejecutar aplicación
CMD ["python", "gestor.py"]
