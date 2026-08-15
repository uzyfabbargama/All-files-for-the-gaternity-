# Usamos una imagen ultra ligera
FROM python:3.11-alpine

# Copiamos el script al contenedor
COPY cifrador.py /app/cifrador.py

# Directorio de trabajo
WORKDIR /app

# Comando por defecto
ENTRYPOINT ["python", "cifrador.py"]
