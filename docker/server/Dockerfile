FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add librdkafka-dev postgresql-libs gcc musl-dev postgresql-dev
COPY requirements.txt .
RUN pip install --requirement requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
