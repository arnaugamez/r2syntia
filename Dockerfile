FROM ubuntu:20.04

RUN apt-get update && \
apt-get -y dist-upgrade && \
apt-get install -y git curl build-essential python3-pip python-is-python3

RUN cd /opt && \
git clone https://github.com/radareorg/radare2.git && \
cd radare2 && \
./sys/install.sh

RUN pip3 install r2pipe orderedset z3-solver

RUN cd /opt && \
mkdir r2syntia

COPY r2syntia.py /opt/r2syntia/r2syntia.py
COPY grammar.def /opt/r2syntia/grammar.def
COPY grammar_full.def /opt/r2syntia/grammar_full.def
COPY syntia /opt/r2syntia/syntia
COPY test_files /opt/r2syntia/test_files

ENTRYPOINT /bin/bash
