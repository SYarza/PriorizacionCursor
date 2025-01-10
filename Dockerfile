# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY solucion_distribucion.py .
COPY dataO2D.json .
COPY requirements.txt .

# Instalar dependencias (si las hubiera)
RUN pip install -r requirements.txt

# Comando para ejecutar el programa
CMD ["python", "solucion_distribucion.py"] 