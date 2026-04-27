FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "cti_project.wsgi:application", "--bind", "0.0.0.0:8000"]