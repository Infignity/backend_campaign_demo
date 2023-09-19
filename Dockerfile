FROM python:3.10-alphine

# send python debugs to terminal
ENV PYTHONUNBUFFERED =1

# set working directory for docker image
WORKDIR /app

# copy the requirements for the app
COPY requirements.txt .

# install requirements for the app
RUN pip install -r requirements.txt

# copy project files to docker app dir
COPY . .

# expose the running port
EXPOSE 8000

# spin the server
ENTRYPOINT [ "/app/django.sh" ]