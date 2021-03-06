import json
import ssl
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from cassandra.policies import DCAwareRoundRobinPolicy
from elasticsearch import Elasticsearch

from meetup.models import Product
from meetup import RESOURCES_DIR

# import logging
# logging.getLogger('cassandra').setLevel(logging.DEBUG)

endpoints = os.environ.get('ELASSANDRA_ENDPOINTS', '127.0.0.1').split(',')
keyspace = os.environ.get('ELASSANDRA_KEYSPACE', 'meetup')
replication_map = json.loads(os.environ.get('ELASSANDRA_RF_MAP', '{"DC1": 1}'))
local_dc = os.environ.get('ELASSANDRA_LOCAL_DC', 'DC1')

config_auth = None
if 'ELASSANDRA_LOGIN' in os.environ:
    config_auth = {
        'username': os.environ.get('ELASSANDRA_LOGIN'),
        'password': os.environ.get('ELASSANDRA_PASSWORD')
    }
    print("using auth")
else:
    config_auth = None

if 'ELASSANDRA_CERTFILE' in os.environ:
    config_ssl = {
        'cacert': os.environ.get('ELASSANDRA_CERTFILE')
    }
    print("using ssl", config_ssl)
else:
    config_ssl = None

already_loaded = False

_es = None
_cql = None


def es():
    return _es


def cql():
    return _cql


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
    print("endpoints ", endpoints)
    connection.setup(endpoints,
                     default_keyspace=keyspace,
                     protocol_version=3,
                     auth_provider=auth_provider,
                     ssl_options=ssl_options,
                     load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=local_dc),
                     retry_connect=True)
    global _cql
    _cql = connection.get_session()

    # Synchronize cassandra schema
    management.create_keyspace_network_topology(keyspace, replication_map)
    management.sync_table(Product, keyspaces=[keyspace])

    # Connection to elasticsearch HTTP
    global _es
    _es = Elasticsearch(endpoints,
                        http_auth=http_auth,
                        scheme=scheme,
                        port=9200,
                        ca_certs=ca_certs,
                        sniff_on_start=False,
                        # refresh nodes after a node fails to respond
                        sniff_on_connection_fail=True,
                        # and also every 60 seconds
                        # sniffer_timeout=60
                        )

    # Create elasticsearch mapping
    # es.indices.delete(index=keyspace)
    if not _es.indices.exists(index=keyspace):
        print("put es mapping")
        mapping_path = os.path.join(RESOURCES_DIR, 'mapping.json')
        _es.indices.create(keyspace, json.loads(open(mapping_path).read()))

    already_loaded = True


if __name__ == '__main__':
    init()
