FROM python:3.7.7-slim-buster
RUN apt-get update && apt-get -y install libmariadb-dev-compat gcc curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python setup.py install