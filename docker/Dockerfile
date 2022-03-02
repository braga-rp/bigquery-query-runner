FROM python:3.8-slim

# docker.io/pedrorangelbraga/bigquery-query-runner

ADD package package

RUN pip3 install --upgrade pip
RUN pip3 install package/*.whl
