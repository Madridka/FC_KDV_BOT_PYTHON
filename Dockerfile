FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt перед установкой
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY main.py ./
COPY static ./static
COPY .env ./
COPY users.json ./

CMD ["python", "main.py"]
