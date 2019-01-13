#!/bin/sh
ENVIRONMENT=${1:-dev}

echo $ENVIRONMENT
docker run -it -v ${PWD}/data:/data --env-file=${ENVIRONMENT}.env folder-watcher
