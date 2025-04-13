FROM python:3.11.4-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=/app/src \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

# Установка Poetry
RUN pip install poetry==2.1.2

# Копирование только зависимостей
COPY pyproject.toml .

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Остальные файлы копируются через volumes в docker-compose

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]