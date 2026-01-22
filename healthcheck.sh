#!/bin/sh

: "${HEALTH_PATH:?Environment variable HEALTH_PATH not set}"

curl -fs --max-time 2 "$HEALTH_PATH" > /dev/null 2>&1 || exit 1

exit 0