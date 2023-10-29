FROM python:3.10-slim

WORKDIR /my_app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./app_requirements.txt .
RUN pip install -r app_requirements.txt

# copy project
COPY . ./my_app