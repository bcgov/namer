#!/bin/bash
# Ported to Dockerfile - not really necessary to call this directly anymore
cd /usr/src/app/namer/static/js/app/
npm install
npm build

cd /usr/src/app/
python namer/wsgi.py
