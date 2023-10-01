# Use Python 3.11 image as a base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# Send Python debugs to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files to the Docker app directory
COPY . /usr/src/app

# Specify the command to run your application (modify this based on your app)
# CMD ["python", "your_main_app_file.py"]
