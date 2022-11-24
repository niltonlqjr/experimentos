#!/bin/bash
source vars.sh

$CONTAINER_CMD build . -t $CONTAINER_IMAGE \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g)

