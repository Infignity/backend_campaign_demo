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