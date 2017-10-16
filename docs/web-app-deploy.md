Intended to be deployed as Flask App, with uwsgi in front, and nginx in front of
that.

All dockerised into a single container following this example and guidance:

https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/

# Upgrading the tiangolo container to serve from a package rather than a module.

This is documented on the tiangolo web site.

Move the main.py to:

    /app/webapp/main.py.

Remove the if __name__ ritual from the bottom of the file.
Create __init__.py in the main dir, containing:

    from .webapp import app

Create __init__.py in the webapp dir (to make it a package)
Edit app/uwsgi.ini to suit

# Static Files and Templates

Live in /app/static/
Live in /app/templates/

The container cited above gets nginx to serve the files from /app/static 
automatically. However, we also code Flask (in main.py) to treat them as static 
so it still works when running the app in dev mode using the "flask" dev server. 
Requests to /static/anything should never reach the flask app in production.
Like this:

    app = Flask('assay-allocation-app', 
            static_folder='/app/static',
            template_folder='/app/templates')

# To Build the Docker Container

Nb. See alternative intstructions later if you want the image to be suitable for
registration with Google Container Registry.

cd assay-alloc
docker build -t assay-alloc-img .

# Deploy Dockerised Locally

docker run -d --name assay-alloc-cont -p 80:80 assay-alloc-img
visit localhost:80

# Deploy Dockerised Locally in Dev Mode
We override the python code served by the container by mounting the app code on 
our local file system over the top of what is in the container.

First you have to create a place in your local filesystem that Docker can see.
E.g.

       c:/shared-with-docker

Then in Windows Docker settings make sure C: is shared with docker.
There can be permissions problems if you use C:/users/you/blah.
C:/shared-with-docker seems to work though.

Test it (having put something in shared-with-docker/data) with a public image:

       docker run -v c:/shared-with-docker:/data alpine find /data

For our app we do this:

       docker run -d --name assay-alloc-cont -p 80:80 \
       -v c:/docker-share/assay-alloc/app:/app \
       assay-alloc-img

Now the container will server files from /shared-with-docker/assay-alloc/app
(But only after Docker stop/start, because the uwsgi component in the image takes
a snapshot when it starts only.

## Get auto code reload

Defeat the operation of supervisord in the image by starting the container like
this:
        docker run -d --name assay-alloc-cont -p 80:80 \
        -v c:/docker-share/assay-alloc/app:/app \
        -e FLASK_APP=main/main.py -e FLASK_DEBUG=1 assay-alloc-img \
        bash -c "while true ; do sleep 10 ; done"

This spins up the container environment but does not start any servers.
You can run (or re-run) flask manually by logging into it:

        docker exec -it assay-alloc-cont bash

Then running the Flask dev server:

        flask run --host=0.0.0.0 --port=80

# Deploying with Kubernetes on Google Cloud Engine

See separate doc - in pete studies: assay-dev-case-study
