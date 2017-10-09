FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

RUN mkdir -p /var/log/uwsgi
