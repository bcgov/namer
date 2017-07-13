FROM python:3-onbuild

RUN apt-get update
RUN curl -sL https://deb.nodesource.com/setup_6.x |  bash -
RUN apt-get install -y nodejs

EXPOSE 5000

RUN chmod ugo+rwx /usr/src/app/docker-start-script.sh
CMD [ "bash", "/usr/src/app/docker-start-script.sh" ]
