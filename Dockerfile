# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9.9-slim-buster

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY *.py  ./
COPY requirements.txt ./requirements.txt
# COPY asciichan ./asciichan/
# COPY blogs/ ./blogs/
COPY mysite/ ./mysite/
COPY theora/ ./theora/
# COPY db_data_pg12 ./db_data_pg12/

# Install production dependencies.
RUN set -ex \
    && pip install -r requirements.txt

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]