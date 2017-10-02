FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install Flask-Shelve

COPY ./app /app
