import json

from flask import Flask, render_template, request, jsonify
from meetup import database, STATIC_DIR, TEMPLATES_DIR
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
        return jsonify({"error": 400, "message": "invalid json body"})

    query = Product.objects(es_query={
        "query": {
            "match": {
                "product_name.ngram": request.get_json().get('q', '')
            }
        }
    })

    return jsonify([p.product_name for p in query.limit(10)])


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    if not request.is_json:
        return jsonify({"error": 400, "message": "invalid json body"})

    body = request.get_json()

    res = es().search(
        index="meetup",
        body={
            "query": {
                "match": {
                    "product_name": body.get('q', '')
                }
            }
        }
    )

    return jsonify(res)


if __name__ == '__main__':
    app.run()
