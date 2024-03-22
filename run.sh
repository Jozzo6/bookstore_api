#!/bin/bash

command="$1"

if [[ $command == "local" ]]; then
    docker-compose -f docker-compose-local.yaml up --build
elif [[ $command == "clean" ]]; then
    docker-compose -f docker-compose-local.yaml stop 
    docker-compose -f docker-compose-local.yaml rm -vf
else 
    echo "Unknown command: $command"
fi