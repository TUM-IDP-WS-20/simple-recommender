FROM python:3.8-slim-buster

RUN apt-get update \
    && apt-get install -y curl build-essential shellcheck

ENV LRS_DIR /app

WORKDIR ${LRS_DIR}

COPY . .

RUN pip3 install -r requirements.txt

# Remove the entrypoint
ENTRYPOINT []
