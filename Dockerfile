# 1. Elige una imagen base de Python ligera
FROM python:3.11-slim

# 2. Evita que pip escriba archivos pycache y la caché de paquetes
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Crea y usa el directorio /app
WORKDIR /app

# 4. Copia solo los requerimientos primero (para aprovechar el cache de Docker)
COPY requirements.txt .

# 5. Instala las dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Copia el resto de tu código
COPY . .

# 7. Expón el puerto en el que corre Uvicorn
EXPOSE 8000

# 8. Comando por defecto al iniciar el contenedor
#    Ajusta "main:app" si tu aplicación FastAPI está en otro módulo
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]