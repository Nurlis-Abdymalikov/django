FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirement.txt /app/requirement.txt

RUN pip install -r /app/requirement.txt

COPY . .