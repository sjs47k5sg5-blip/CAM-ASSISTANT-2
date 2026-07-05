FROM python:3.11-slim

# Рабочая папка
WORKDIR /app

# Устанавливаем зависимости системы (важно для aiohttp)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем проект
COPY . /app

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "bot.py"]