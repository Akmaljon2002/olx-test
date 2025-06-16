FROM python:3.12.4-slim

# OS darajasidagi zarur kutubxonalarni o‘rnatamiz
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Requirements faylni ko‘chirib o‘rnatamiz
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Xavfsizlik: oddiy user yaratamiz
RUN useradd -m nonroot
USER nonroot

# Loyihani ichiga ko‘chiramiz
COPY . /code
WORKDIR /code

# Portni ochamiz
EXPOSE 8080

# Gunicorn orqali ishga tushiramiz
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} --access-logfile - core.wsgi:application --workers 3 --timeout 120

