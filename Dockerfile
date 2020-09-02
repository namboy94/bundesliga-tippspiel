FROM ubuntu:20.04
MAINTAINER Hermann Krumrey <hermann@krumreyh.com>

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y python3 python3-pip python3-psycopg2 && \
    pip3 install flask

RUN apt install git -y && git clone https://gitlab.namibsun.net/namibsun/python/puffotter.git -b develop && cd puffotter && pip3 install .[flask]

ADD . flask-app
RUN cd flask-app && python3 setup.py install

WORKDIR flask-app
CMD ["/usr/bin/python3", "server.py"]
