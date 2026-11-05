FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production \
    FLASK_APP=informatics_front.wsgi:application

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./
COPY migrations ./migrations
COPY informatics_front ./informatics_front

RUN useradd --system --no-create-home app
USER app

EXPOSE 12347

# 60s matches the timeout of the calls to the rmatics core (see InternalRmatics).
CMD ["gunicorn", "--bind", "0.0.0.0:12347", "--workers", "4", "--timeout", "60", \
     "--access-logfile", "-", "informatics_front.wsgi:application"]
