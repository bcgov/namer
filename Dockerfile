FROM python:3-onbuild
ENV PYTHONUNBUFFERED 1

# Install NodeJS
# RUN apt-get update  # Not needed since the setup_8.x script runs this already
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

EXPOSE 5000

# Build NPM
WORKDIR /usr/src/app/namer/static/js/app/
RUN npm install
RUN npm run build

# Start Server
WORKDIR /usr/src/app/
RUN chmod 744 -R /usr/src/app/namer/static/js/app/node_modules
CMD [ "python", "namer/wsgi.py" ]

# RUN chmod ugo+rwx /usr/src/app/docker-start-script.sh
# CMD [ "bash", "/usr/src/app/docker-start-script.sh" ]
