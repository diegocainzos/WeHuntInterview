# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Evita que Python escriba archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que Python haga buffering en stdout y stderr
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar ciertos paquetes
RUN apt-get update && apt-get install -y 
    build-essential 
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone los puertos para FastAPI (8000) y Streamlit (8501)
EXPOSE 8000 8501

# Por defecto, ejecuta el dashboard interactivo de Streamlit
# Si prefieres levantar la API, puedes sobreescribir este comando al hacer docker run con:
# uvicorn src.server:app --host 0.0.0.0 --port 8000
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
