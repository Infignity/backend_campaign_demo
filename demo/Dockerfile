# Use Python 3.11 image as a base image
FROM python:3.11.4-buster

# Send Python debugs to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat \
    redis

# set work directory
WORKDIR /usr/src/app

# Copy the requirements for the app
COPY requirements.txt .

# Update pip
RUN pip install --upgrade pip

# Install requirements for the app
RUN pip3 install -r requirements.txt

# Copy project files to the Docker app directory
COPY . .

# Specify the command to run your application (modify this based on your app)
# CMD ["python", "your_main_app_file.py"]
