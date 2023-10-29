FROM python:3.10-slim
WORKDIR /api

COPY ./api_requirements.txt .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y wget curl
# install dependencies
RUN pip install --upgrade pip

RUN pip3 install -r api_requirements.txt

COPY . ./rest_api




