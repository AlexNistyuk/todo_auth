FROM python:3.11.7-slim-bookworm

RUN mkdir /fastapi_todo_auth
WORKDIR /fastapi_todo_auth

RUN pip3 install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync --system

COPY . .
