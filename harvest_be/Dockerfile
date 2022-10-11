FROM python:3.7

ARG ENV

WORKDIR /code

COPY requirements/base.txt /code/

RUN pip install -r base.txt
ADD . /code/
