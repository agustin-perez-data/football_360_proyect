FROM python:3.11-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala psql (cliente de postgres) + dependencias básicas
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Setea el working directory
WORKDIR /app

# Copia requirements e instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto (opcional, igual usás volumen)
# COPY . .

# Mantiene el contenedor vivo para ejecutar comandos
CMD ["sleep", "infinity"]
