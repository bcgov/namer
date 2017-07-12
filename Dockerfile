FROM python:3-onbuild

EXPOSE 9000

ENV FLASK_APP=wsgi.py

CMD [ "python", "corpnamesregistry/wsgi.py"]