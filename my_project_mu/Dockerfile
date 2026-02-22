# Базовый образ с нужной версией Python
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]

