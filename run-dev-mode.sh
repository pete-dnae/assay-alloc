#!/bin/bash

docker stop xxx-cont
docker rm xxx-cont

# Run container with mounted volume, but override startup behaviour to defeat
# running of uwsgi and nginx, and instead just run a keep-alive loop.

# Then later can get interactive session into container with
# docker exec -it xxx-cont bash

# And from inside start / restart flask directly with:
# flask run --host=0.0.0.0 --port=80

docker run -d --name xxx-cont -p 80:80 \
-v c:/docker-share/assay-alloc/app:/app \
-e FLASK_APP=main/main.py -e FLASK_DEBUG=1 \
xxx-img \
bash -c "while true ; do sleep 10 ; done"
