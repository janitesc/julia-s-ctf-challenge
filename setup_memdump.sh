#!/bin/bash
set -e

cd "$(dirname "$0")"

IMAGE_NAME="julia-ctf"
CONTAINER_NAME="julia-container"

echo "building docker image" 
docker build -t "$IMAGE_NAME" -f Dockerfile.dev .

echo "removing old container"
docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true


echo "starting new container in backgrround"
docker run -d --name "$CONTAINER_NAME" "$IMAGE_NAME" >/dev/null

echo "waiting for a bit so the memdump is generated"
sleep 5

#finding memdump 
DUMP_NAME=$(docker exec "$CONTAINER_NAME" /bin/bash -lc 'cd /challenge && ls memdump.* 2>/dev/null | head -n1')

if [ -z "$DUMP_NAME" ]; then
  echo "No memdump found in container!"
  exit 1
fi

echo "Copying memdump to host as memdump.bin"
docker cp "$CONTAINER_NAME:/challenge/$DUMP_NAME" ./memdump.bin

echo "Done.    - Container '$CONTAINER_NAME' is still running (server)."

