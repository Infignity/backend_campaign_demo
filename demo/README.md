# backend_campaign_demo


### MAC/LINUX USERS
```
# Create virtual env
python3 -m venv env
# activate enviroment
source env/bin/activate
```

####  for django app creation for all users
```
#  for fresh app creations
python3 -m pip install Django openai langchain

# check django version
django-admin --version

# create django app
django-admin startproject my_app

```

### for running this current created app

```
# if not in demo directory change directory into demo
cd demo

# install requirements
pip3 install -r requirements.txt

# run the server
python3 manage.py runserver
```


# create postgress user
```
psql postgres
# create database
CREATE DATABASE campaign_demo;

# creating the user project
CREATE USER project WITH ENCRYPTED PASSWORD 'project123';

# grant permission to created user on the database
GRANT ALL PRIVILEGES ON DATABASE campaign_demo TO project;

```


## Running Celery MAC Users
```
# ensure redis cli is running and installed
brew services list

# if not install
brew install redis

# verify redis installation
redis-server

# start the redis cli
brew services start redis

cd demo
python3 -m celery -A demo.celery worker --loglevel=info
```


## docker spin up

```
# start up the database
docker-compose up --build

# to check running db image
docker ps -a


# create the database
docker-compose exec db psql --username=demo --dbname=demo

# inspect the volume
docker volume inspect django-on-docker_postgres_data

# check the network 
docker network ls

# check the volumes
docker volumes ls

# stop the docker service
docker-compose down

# first remove the image before pruning
docker rmi img_id

# delete the volumes
docker prune

# prevent starting of container on every container start or re-start:
docker-compose exec app python manage.py flush --no-input
docker-compose exec app python manage.py migrate

```

# major dependencies

1. celery
2. redis
3. Elastic Search
4. langchain
5. openAI