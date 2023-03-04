FROM python:3.10.10-slim-bullseye AS builder

ENV TZ Asia/Shanghai

WORKDIR /app

COPY . /app

RUN [pip install -r requirements.txt]
