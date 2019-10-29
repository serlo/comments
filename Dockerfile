FROM python:3.8-alpine

WORKDIR /usr/src/app
COPY requirements.txt .
# RUN apt-get update -y
# RUN apt-get install -y software-properties-common
# RUN wget -qO - https://packages.confluent.io/deb/5.3/archive.key | apt-key add -
# RUN add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/5.3 stable main"
# RUN apt-get update -y
# RUN apt-get install -y librdkafka-dev python-dev
RUN apk add librdkafka-dev postgresql-libs gcc musl-dev postgresql-dev
RUN pip install --requirement requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
