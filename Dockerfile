FROM python:3.8-alpine

WORKDIR /usr/src/app
COPY requirements.txt .
RUN apk add librdkafka-dev postgresql-libs gcc musl-dev postgresql-dev
RUN pip install --requirement requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
