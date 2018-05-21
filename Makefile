
all: build

build:
	docker build --rm -t "strapdata/meetup:0.1" .

publish: build
	docker push strapdata/meetup:0.1

up:
	docker-compose -f docker-compose-meetup-dev.yml up -d

down:
	docker-compose -f docker-compose-meetup-dev.yml down
