# Python Meetup

**Require python3**

## Standelone

Install the dependencies:

    pip install -r requirements.txt
    export PYTHONPATH="$(pwd)"

Import the data from Open Food Fact CSV:

    wget https://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv -O fr.openfoodfacts.org.products.csv
    python3 -m meetup.import

Start the web server:
    
    python3 -m meetup.web
    
## Dockerized 

Build the docker image:

    make build

Run a docker container including the application, the importer and kibana:

    make up
    
Stop the docker container:

    make down

Check application logs:

    make logs

Open a shell in the web container:

    make shell
    
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
