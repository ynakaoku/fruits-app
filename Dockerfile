#FROM python:3.5.2
FROM python:3.11

# RUN groupadd web
# RUN useradd -d /home/python -m python

RUN mkdir /home/python
WORKDIR /home/python
# ADD cgiserver.py .
RUN wget https://raw.githubusercontent.com/ynakaoku/fruits-app/main/cgiserver.py
#ADD index.html /home/python
RUN mkdir fruits
#ADD index.cgi ./fruits
RUN wget https://raw.githubusercontent.com/ynakaoku/fruits-app/main/index.cgi
RUN mv index.cgi ./fruits
RUN chmod 755 ./fruits/index.cgi

RUN apt-get -y update
RUN apt-get -y install wget unzip iputils-ping
RUN apt-get -y install python3-pip
RUN python -m pip install pymongo

EXPOSE 80
ENTRYPOINT ["/usr/local/bin/python", "/home/python/cgiserver.py"]
# USER python
