FROM python:3.12-slim
LABEL authors="emtsev_sound"

WORKDIR /app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requrements.txt

COPY . .