#!/bin/bash

command="$1"

if [[ $command == "local" ]]; then
    docker-compose -f docker-compose-local.yaml up --build
elif [[ $command == "db" ]]; then
    cd database
    if [ $(docker ps -a -q -f name=bookstore) ]; then
        docker start bookstore
    else
        docker build -t bookstore_image .
        docker run --name bookstore -e POSTGRES_PASSWORD=testing -p 5432:5432 -d bookstore_image
    fi
elif [[ $command == "clean" ]]; then
    docker-compose -f docker-compose-local.yaml stop 
    docker-compose -f docker-compose-local.yaml rm -vf

    docker rm -f bookstore
    docker rmi -f bookstore_image 
else 
    echo "Unknown command: $command"
fi