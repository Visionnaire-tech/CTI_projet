FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install django psycopg2-binary pandas openpyxl

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]