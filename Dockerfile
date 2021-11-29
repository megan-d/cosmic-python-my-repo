# This dockerfile is for the app image. The postgres image we will get directly from DockerHub.

FROM python:3.9-slim-buster

# RUN apt install gcc libpq (no longer needed bc we use psycopg2-binary)


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt


RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/


WORKDIR /src
ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_ENV=development FLASK_DEBUG=1 PYTHONUNBUFFERED=1 PYTHONPATH="${PYTHONPATH}:/src/allocation"
CMD flask run --host=0.0.0.0 --port=80