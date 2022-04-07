# https://gitlab.cern.ch/jawieczo/isolationverifier/-/blob/master/opc/docker/server/Dockerfile

FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        vim \
        telnet \
        wget \
        iputils-ping \
        python3 \
        python3-pip \
        usbutils \
        libxml2-dev \
        libxslt1-dev \
    && pip3 install opcua
