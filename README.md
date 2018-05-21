# Python Meetup

**Require python3**

## Standelone

Get the Open Food Fact CSV :

    wget https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv -O fr.openfoodfacts.org.products.csv

Install the dependencies:

    pip install -r requirements.txt

Import the data:

    python3 -m meetup.import


Start the web server:

    python3 -m meetup.web


## Dockerized 

Build the docker image:

    make build

Run a docker container including the application and kibana:

    make up
    
Stop the docker container:

    make down

Check application logs:

    docker logs pymeetup_meetup_1

Run a bash in the docker container:

    docker exec -it pymeetup_meetup_1 bash
    
## Usage

* webapp [http://localhost:5000](http://localhost:5000)
* kibana [http://localhost:5601](http://localhost:5601)

## References

* [Open Food Facts](https://world-fr.openfoodfacts.org/)
* [Docker for python applications](http://tiborsimko.org/docker-for-python-applications.html)
* [Python cassandra driver](https://datastax.github.io/python-driver/index.html)
* [Python elasticsearch driver](https://elasticsearch-py.readthedocs.io/en/master/index.html)
* [Elassandra documentation](http://doc.elassandra.io/en/latest/enterprise.html#multi-user-kibana-configuration)
* [Cassandra COPY CSV](https://docs.datastax.com/en/cql/3.3/cql/cql_reference/cqlshCopy.html)
* [Configuring Kibana on Docker](https://www.elastic.co/guide/en/kibana/current/_configuring_kibana_on_docker.html)
    