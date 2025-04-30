# Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

CMD gunicorn blogs.wsgi --bind 0.0.0.0:$PORT