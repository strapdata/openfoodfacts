
COMPOSE_FILE = docker-compose-local-linux.yml
IMAGE_NAME= strapdata/openfoodfacts
VERSION = 0.1

all: build

build:
	docker build --rm -t "$(IMAGE_NAME):$(VERSION)" .

publish: build
	docker push $(IMAGE_NAME):$(VERSION)

up:
	docker-compose -f $(COMPOSE_FILE) up -d

down:
	docker-compose -f $(COMPOSE_FILE) down
