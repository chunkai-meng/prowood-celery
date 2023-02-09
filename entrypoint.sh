#!/bin/bash

trap "echo ''" SIGINT

count=2

gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 proj.asgi:application -k uvicorn.workers.UvicornWorker &

celery -A proj worker --beat --scheduler django -l info &

wait

while true
do
    for ((i=0; i<count; i++))
    do
        kill $[ $! - $i ]
    done
    exit
done
