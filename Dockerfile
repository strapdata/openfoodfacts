FROM ubuntu:latest
MAINTAINER Barthelemy Delemotte "barth@strapdata.com"
RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

ADD ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT "/docker-entrypoint.sh"

COPY ./meetup/* /meetup/
COPY ./resources/* /resources/
COPY ./static/* /static/
COPY ./templates/* /templates/


