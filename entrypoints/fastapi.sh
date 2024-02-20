#!/bin/bash

cd src

uvicorn main:app --host $WEB_CONTAINER_HOST --port $WEB_PORT --workers $WORKERS
