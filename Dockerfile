FROM python:3.12.0a6-slim AS build

RUN mkdir -p /app
WORKDIR /app
COPY src src
COPY setup.py setup.py
COPY README.md README.md
COPY LICENSE LICENSE
COPY install.sh install.sh
RUN mkdir -p ~/.jira_metrics
RUN ./install.sh

ENTRYPOINT [ "metrics" ]