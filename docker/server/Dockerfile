FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add librdkafka-dev gcc musl-dev postgresql-dev postgresql-libs
COPY requirements.txt .
RUN pip install --requirement requirements.txt
COPY app app
COPY pact pact
COPY threads threads
COPY manage.py .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
