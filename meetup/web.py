import json

from flask import Flask, render_template, request, jsonify
from meetup import database
from meetup import STATIC_DIR, TEMPLATES_DIR
from meetup.database import es
from meetup.models import Product

database.init()
app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR, static_url_path='/static')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    if not request.is_json:
        return jsonify({"error": 400, "message": "invalid json body"}), 400

    query = Product.objects(es_query={
        "query": {
            "match": {
                "product_name.ngram": request.get_json().get('q', '')
            }
        }
    })

    return jsonify([p.product_name for p in query.limit(10)])


@app.route('/api/autocomplete_agg', methods=['GET', 'POST'])
def autocomplete_agg():
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

    cql_query = "SELECT * FROM {}.product WHERE es_query='{}'".format(database.keyspace, json.dumps(es_query))
    result = [row['product_name.key'] for row in database.cql().execute(cql_query)]

    return jsonify(result)


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    if not request.is_json:
        return jsonify({"error": 400, "message": "invalid json body"}), 400

    body = request.get_json()

    res = es().search(
        index=database.keyspace,
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


@app.route('/api/product', methods=['GET'])
def get_product():
    code = request.args.get('code', default=1, type=str)
    product = Product.objects(code=code).first().to_dict()
    return jsonify(product)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
