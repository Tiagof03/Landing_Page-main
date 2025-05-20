# Usa una imagen base de Python. Puedes elegir una versión específica de Python.
# python:3.9-slim-buster es una buena opción por su tamaño reducido.
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
# Primero copia solo requirements.txt para aprovechar el cache de Docker
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del proyecto al directorio de trabajo del contenedor
# Esto incluye app.py, database.py, templates/, css/, JS/, img/, iconos-productos/
COPY . .

# Expone el puerto en el que la aplicación Flask se ejecutará
EXPOSE 5000

# Comando para inicializar la base de datos (se ejecuta solo una vez al construir la imagen)
# Esto es útil si tu DB solo necesita crearse una vez con su esquema.
# Para escenarios más complejos (migraciones), podría manejarse diferente.
RUN python3 database.py

# Define el comando que se ejecutará cuando se inicie el contenedor
# 'flask run' es para desarrollo. En producción, usarías un WSGI como Gunicorn.
CMD ["python3", "app.py"]