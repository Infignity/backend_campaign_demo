# Use the official Python 3.10 image as a base image
FROM python:3.11.4-buster

# Send Python debugs to terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install build-essential and other dependencies
RUN apt-get update && apt-get install -y build-essential

# set work directory
WORKDIR /usr/src/app

# Copy the requirements for the app
COPY requirements.txt .

# update pip
RUN pip install --upgrade pip

# Install requirements for the app
RUN pip3 install -r requirements.txt


# copy django.sh
COPY ./django.sh .
RUN sed -i 's/\r$//g' /usr/src/app/django.sh
RUN chmod +x /usr/src/app/django.sh

# Copy project files to the Docker app directory
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/django.sh"]