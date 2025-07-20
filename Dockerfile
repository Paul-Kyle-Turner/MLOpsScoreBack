FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

ARG _BRANCH_NAME=main

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD gunicorn -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 main:app
