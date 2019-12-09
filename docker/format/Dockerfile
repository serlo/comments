FROM python:3.8-alpine

WORKDIR /usr/src/app
RUN apk update && apk add gcc musl-dev
COPY requirements-dev.txt .
RUN pip install --requirement requirements-dev.txt

CMD ["black", ".", "--target-version", "py38"]
