# syntax=docker/dockerfile:1
FROM python:3.9.6-slim

COPY . /app
WORKDIR /app

EXPOSE 8080

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT gunicorn main:app -b :8080