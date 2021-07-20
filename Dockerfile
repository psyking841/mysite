# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY *.py  ./
COPY asciichan ./asciichan/
COPY blogs/ ./blogs/
COPY mysite/ ./mysite/
COPY db_data ./db_data/

# Install production dependencies.
RUN pip install Django psycopg2-binary django-environ

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]