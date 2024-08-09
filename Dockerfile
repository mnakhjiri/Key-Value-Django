FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 # Prevents Python from buffering stdout and stderr
ENV SHELL /bin/bash

WORKDIR /app

RUN mkdir -p /run/daphne && \
    apt-get update && \
    apt-get install ffmpeg -y && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 8000
