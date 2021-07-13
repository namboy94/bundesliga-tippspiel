FROM ubuntu:20.04
MAINTAINER Hermann Krumrey <hermann@krumreyh.com>

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y python3 python3-pip python3-psycopg2 \
    ruby-sass npm yui-compressor && \
    pip3 install flask

RUN pip3 install bundesliga_tippspiel && pip3 uninstall bundesliga_tippspiel -y
RUN pip3 install jerrycan --upgrade

ADD . flask-app
RUN cd flask-app && python3 setup.py install

WORKDIR flask-app
CMD ["/usr/bin/python3", "server.py"]
