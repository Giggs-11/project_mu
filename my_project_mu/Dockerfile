FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    -o Acquire::Retries=3 \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app


RUN pip install --no-cache-dir poetry pymysql


COPY pyproject.toml poetry.lock* ./


RUN poetry config virtualenvs.create false \
    && (poetry install --no-interaction --no-ansi --no-root || pip install django django-environ)

COPY . .


EXPOSE 8000
WORKDIR /app/src


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
