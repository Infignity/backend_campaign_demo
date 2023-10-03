# pull official base image
FROM python:3.9-alpine as base

LABEL maintainer="wrefordmessi@gmail.com"

# set work directory
WORKDIR /app


COPY ./requirements.txt .
RUN apk add --no-cache --virtual --upgrade build-base linux-headers && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Now multistage build
FROM python:3.9-alpine
RUN apk add libpq
COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .
