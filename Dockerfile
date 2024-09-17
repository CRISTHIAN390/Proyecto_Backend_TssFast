# Usa la imagen python:3.12.6-slim como base
FROM python:3.12.6-bullseye

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu aplicación
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la API al contenedor
COPY . .

# Expone el puerto 4500, que es el puerto en el que la aplicación FastAPI escuchará
EXPOSE 4500

# Define el comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4500"]