FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt

ADD ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT "/docker-entrypoint.sh"

COPY ./docker-context.sh /etc/profile.d/
COPY ./meetup/* /meetup/
COPY ./resources/* /resources/
COPY ./static/* /static/
COPY ./templates/* /templates/
