FROM python:3.6
ENV PYTHONUNBUFFERED 1
EXPOSE 5000

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

# Install Project Requirements
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# Build NPM Dependencies
COPY namer/static/js/app/package.json /usr/src/app/namer/static/js/app/
WORKDIR /usr/src/app/namer/static/js/app/
RUN npm install
RUN chmod -R 777 node_modules

# Copy and Compile Angular Code
COPY namer/static /usr/src/app/namer/static
RUN npm run build

# Copy remaining Source Code
COPY . /usr/src/app

# Start Server
WORKDIR /usr/src/app/
CMD [ "python", "namer/wsgi.py" ]
