FROM python:3.8

WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --requirement requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
