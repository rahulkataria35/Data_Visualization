FROM tiangolo/uwsgi-nginx-flask:python3.8

LABEL maintainer="Rahul Kataria <rahul.kataria@saarathi.ai>"

ADD ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

RUN apt-get -y update
RUN apt-get install -y build-essential

COPY ./app /app
WORKDIR /app
EXPOSE 80
