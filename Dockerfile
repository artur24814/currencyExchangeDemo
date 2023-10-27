FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# install mysql dependencies
RUN apt-get update && \
    apt-get install -y pkg-config && \
    apt-get install gcc default-libmysqlclient-dev -y

COPY requirements.txt /requirements.txt
COPY ./app /app

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install -U pip setuptools wheel && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"
