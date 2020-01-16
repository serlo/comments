FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add librdkafka-dev postgresql-libs gcc musl-dev postgresql-dev
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --requirement requirements.txt
RUN pip install --requirement requirements-dev.txt
