Integrating Elassandra in your Python application
=================================================

This tutorial aims to demonstrate how to integrate Elassandra in your Python code.

For this purpose, we will build a simple web application that handles a catalog of food products, and provides search and autocomplete features.

We are not covering the installation and configuration of Elassandra. So we assume you already have an Elassandra instance running.

There is no specific Elassandra driver for Python. We make use of the existing [cassandra]() or [elasticsearch]() drivers.

## Model your data

With the cassandra driver, we can model the data in the same way we would do with an ORM.

```python
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import Text, DateTime


class Product(Model):
    code = Text(primary_key=True)
    url = Text()
    created_t = DateTime()
    product_name = Text()
    
```

And then we can synchronize this model with the actual database schema :
```python
from cassandra.cqlengine import connection
from cassandra.cqlengine import management
from cassandra.policies import DCAwareRoundRobinPolicy

keyspace="app"
connection.setup(["127.0.0.1"], default_keyspace=keyspace, protocol_version=3,
                     load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='DC1'),
                     retry_connect=True)
                     
management.create_keyspace_network_topology(keyspace, {'DC1': 1})
management.sync_table(Product, keyspaces=[keyspace])
```

Two things to note: 
* the driver will not remove existing columns, but only add new ones ;
* by setting a `load_balancing_policy`, the driver will always try to connect the local datacenter first, and if it goes offline, it will try the other ones.


That's good enough for our simple app.

## Index your data

Now that we have seen the cassandra side of elassandra, we are going to show how to add an elasticsearch index upon the cassandra table.

We wanted to build a food product search engine with autocompletion. So we need to define an elasticsearch mapping with such facilities.

Let's create a `mapping.json` file :
```json
{
    "settings": {
    "index": {
      "analysis": {
        "filter": {},
        "analyzer": {
          "edge_ngram_analyzer": {
            "filter": [
              "lowercase"
            ],
            "tokenizer": "edge_ngram_tokenizer"
          },
          "edge_ngram_search_analyzer": {
            "tokenizer": "lowercase"
          }
        },
        "tokenizer": {
          "edge_ngram_tokenizer": {
            "type": "edge_ngram",
            "min_gram": 2,
            "max_gram": 20,
            "token_chars": [
              "letter"
            ]
          }
        }
      }
    }
  },
  "mappings": {
    "product": {
      "discover":"^((?!product_name).*)",
      "properties": {
        "product_name": {
          "type": "text",
          "cql_collection": "singleton",
          "fields": {
            "keyword": {
              "type": "keyword"
            },
            "ngram": {
              "type": "text",
              "analyzer": "edge_ngram_analyzer",
              "search_analyzer": "edge_ngram_search_analyzer"
            }
          }
        }
      }
    }
  }
}
```

In this mapping, we said we wanted to index the `product_name` using both full-text, edge_ngram, and keyword analyzer.
Then, we used the special `discover` properties to tell elassandra we want to index all other columns using reasonable defaults.

Now we want to PUT this mapping whenever the python app starts :
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["127.0.0.1"], scheme="http", sniff_on_connection_fail=True)

if not es.indices.exists(index=keyspace):
    es.indices.create(keyspace, json.loads(open('./mapping.json').read()))
```

## Query your data

We used Flask to create webservices serving the data from Elassandra.

```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='./templates', static_folder='./static', static_url_path='/static')
```

We want three routes in our API :
* one to access a product details page
* one for the search
* one for the autocompletion

For each route, we will use a different approach.

### Pure cassandra query - Read a single product

This is the simplest query. It takes a product ean code and returns the product details :
```python
from flask import request, jsonify

@app.route('/api/product', methods=['GET'])
def get_product():
    code = request.args.get('code', default="1", type=str)
    product = dict(Product.objects(code=code).first())
    return jsonify(product)
```

We did not write a CQL statement manually, we rather used the object mapper.

### Pure elasticsearch query - Search for products

The search route takes a string as parameter and uses it for a full-text search upon the `product_name` column :
```python
@app.route('/api/search', methods=['GET', 'POST'])
def search():
    if not request.is_json:
        return jsonify({"error": 400, "message": "invalid json body"}), 400

    body = request.get_json()

    res = es.search(
        index=keyspace,
        body={
            "query": {
                "match": {
                    "product_name": body.get('q', '')
                }
            }
        },
        size=20
    )

    return jsonify(res)
```

We used the elasticsearch REST driver for this query.


### Mixed elasticsearch over CQL query - Autocompletion

The last route is much trickier. We want that, giving the input string "Chick",
the response suggests product names such as "Chicken", "Chick Peas", "Chicken Sausage", "Chicken Wings", and more...

The query is based on an elasticsearch aggregation query on the `product_name` field analyzed as `edge_ngrams`.
```python
es_query = {
        "size": 0,
        "query": {
            "match": {
                "product_name.ngram": request.get_json().get('q', '')
            }
        },
        "aggs": {
            "product_name": {
                "terms": {
                    "field": "product_name.keyword",
                    "size": 10
                }
            }
        }
    }
```

Furthermore, we are going to embed the elasticsearch query directly in the CQL statement.

This option is only available in the [Elassandra Enterprise]() plugin.

So the complete code of this route is :
```python
session = connection.get_session()

@app.route('/api/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    if not request.is_json:
        return jsonify({"error": 400, "message": "invalid json body"}), 400

    es_query = {
        "size": 0,
        "query": {
            "match": {
                "product_name.ngram": request.get_json().get('q', '')
            }
        },
        "aggs": {
            "product_name": {
                "terms": {
                    "field": "product_name.keyword",
                    "size": 10
                }
            }
        }
    }

    cql_query = "SELECT * FROM {}.product WHERE es_query='{}'".format(keyspace, json.dumps(es_query))
    result = [row['product_name.key'] for row in session.execute(cql_query)]

    return jsonify(result)
```

If you're interested testing this feature, we provide free 30-days trial.


## Finally

We imported the data from a csv export of the opensource project [openfoodfact]().

The complete code, including HTML/CSS and jquery is available on [github]().




