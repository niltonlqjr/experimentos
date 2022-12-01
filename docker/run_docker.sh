source ./vars.sh

$CONTAINER_CMD run --interactive --tty --rm \
  --env "HOME=$VOLUME_DIR" \
  --env "SHELL=/bin/bash" \
  --workdir $VOLUME_DIR \
  --volume $VOLUME_DIR:$VOLUME_DIR \
  --user "$(id -u):$(id -g)" \
  --security-opt seccomp=${WORK_DIR}/perf_event_open.json \
  --privileged \
  $CONTAINER_IMAGE "$@"
