# pull base image
FROM python:3.7-slim

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# install dependency
COPY requirement.txt /code/
RUN pip install -r requirement.txt

# Copy project
COPY . /code

