FROM python:3-onbuild

EXPOSE 5000

ENV FLASK_APP=wsgi.py

CMD [ "python", "corpnamesregistry/wsgi.py"]
