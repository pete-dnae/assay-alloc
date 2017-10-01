#!/bin/bash

export FLASK_APP=./app/main/main.py
export FLASK_DEBUG=1
python -m flask run
