#!/bin/bash

cd src

uvicorn main:app --reload --host $WEB_CONTAINER_HOST --port $WEB_PORT
