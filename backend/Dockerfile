FROM python:3.13
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir gunicorn==20.1.0 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kinoz.wsgi"]