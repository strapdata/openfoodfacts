import json

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class EsQuery(columns.Text):
    """
    Dummy column used to make elasticsearch queries from within CQL :
        `SELECT * FROM keyspace.table where es_query='{ "query": { "match_all": { } } }'`
    """

    def __init__(self):
        super().__init__(custom_index=True)

    def to_database(self, value):
        if type(value) is dict:
            value = json.dumps(value)
        return value

    def to_python(self, value):
        return None


class Product(Model):
    code = columns.BigInt(primary_key=True)
    url = columns.Text()
    product_name = columns.Text()
    brands = columns.Text()
    image_url = columns.Text()
    es_query = EsQuery()

    def to_dict(self):
        json_dict = dict(self)
        del json_dict['es_query']
        return json_dict
