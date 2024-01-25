#!/bin/bash

cd src

alembic upgrade head

uvicorn main:app --host $WEB_CONTAINER_HOST --port $WEB_PORT --workers $WORKERS
