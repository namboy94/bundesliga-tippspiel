FROM ubuntu:18.04
MAINTAINER Hermann Krumrey <hermann@krumreyh.com>

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y python3 python3-pip python3-mysqldb && \
    pip3 install Flask cherrypy

ADD . flask-app

RUN cd flask-app && python3 setup.py install

WORKDIR flask-app

EXPOSE 8000

CMD ["/usr/bin/python3", "server.py"]
