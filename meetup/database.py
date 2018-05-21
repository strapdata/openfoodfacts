import json
import ssl
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from elasticsearch import Elasticsearch

from meetup.models import Product
from meetup import RESOURCES_DIR

keyspace = 'meetup'
endpoints = ['LOCAL_ELASSANDRA_RPC']

#config_auth = None
config_auth = { 'username': 'LOCAL_ELASSANDRA_LOGIN', 'password': 'LOCAL_ELASSANDRA_PASSWORD' }

config_ssl = None
#config_ssl = { 'cacert': 'LOCAL_ELASSANDRA_CERTFILE' }

already_loaded = False

_es = None


def es():
    return _es


def init():
    global already_loaded
    if already_loaded:
        return

    # Authentication configuration
    if config_auth is not None:
        auth_provider = PlainTextAuthProvider(username=config_auth['username'], password=config_auth['password'])
        http_auth = (config_auth['username'], config_auth['password'])
    else:
        auth_provider = None
        http_auth = None

    # Encryption configuration
    if config_ssl is not None:
        ssl_options = {'ssl_version': ssl.PROTOCOL_TLSv1_2, 'ca_certs': config_ssl['cacert']}
        scheme = "https"
        ca_certs = config_ssl['cacert']
    else:
        ssl_options = None
        scheme = "http"
        ca_certs = None

    # Connection to cassandra
    connection.setup(endpoints,
                     default_keyspace=keyspace,
                     protocol_version=3,
                     auth_provider=auth_provider,
                     ssl_options=ssl_options)

    # Synchronize cassandra schema
    management.create_keyspace_network_topology(keyspace, {'DC1': 1})
    connection.execute(open(os.path.join(RESOURCES_DIR, 'schema.cql')).read())
    management.sync_table(Product, keyspaces=[keyspace])

    # Connection to elasticsearch HTTP
    global _es
    _es = Elasticsearch(endpoints,
                        http_auth=http_auth,
                        scheme=scheme,
                        port=9200,
                        ca_certs=ca_certs)

    # Create elasticsearch mapping
    # es.indices.delete(index=keyspace)
    if not _es.indices.exists(index=keyspace):
        print("put es mapping")
        mapping_path = os.path.join(RESOURCES_DIR, 'mapping.json')
        _es.indices.create(keyspace, json.loads(open(mapping_path).read()))

    already_loaded = True


if __name__ == '__main__':
    init()
