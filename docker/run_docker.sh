source ./vars.sh

$CONTAINER_CMD run --interactive --tty --rm \
  --env "HOME=$VOLUME_DIR" \
  --env "SHELL=/bin/bash" \
  --workdir $VOLUME_DIR \
  --volume $VOLUME_DIR:$VOLUME_DIR \
  --user "$(id -u):$(id -g)" \
  $CONTAINER_IMAGE "$@"
