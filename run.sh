#!/bin/bash

command="$1"


start_db() {
    if [ $(docker ps -a -q -f name=bookstore) ]; then
        echo "Starting database..."
        docker start bookstore
    else
        echo "Database container does not exist. Building and starting..."
        docker build -t bookstore_image ./database
        docker run --name bookstore -e POSTGRES_PASSWORD=testing -p 5432:5432 -d bookstore_image
    fi
}

if [[ $command == "local" ]]; then
    docker-compose -f docker-compose-local.yaml up --build
elif [[ $command == "db" ]]; then
    start_db
elif [[ $command == "clean" ]]; then
    docker-compose -f docker-compose-local.yaml stop 
    docker-compose -f docker-compose-local.yaml rm -vf

    docker rm -f bookstore
    docker rmi -f bookstore_image 
elif [[ $command == "test" ]]; then
    start_db

    echo "Waiting for database to start..."
    until docker exec -it bookstore pg_isready -U postgres; do
        sleep 1
    done

    echo "Running tests..."
    pytest
else 
    echo "Unknown command: $command"
fi