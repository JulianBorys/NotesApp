# Używamy oficjalnego obrazu Pythona
FROM python:3.11-slim

# Instalujemy zależności systemowe dla psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy plik requirements.txt do kontenera
COPY requirements.txt .

# Instalujemy zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą aplikację do kontenera
COPY . .

# Ustawiamy zmienną środowiskową dla Django
ENV DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/mydatabase

# Ustalamy port, na którym aplikacja będzie działać
EXPOSE 8000

# Uruchamiamy aplikację Django (przykład dla development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
