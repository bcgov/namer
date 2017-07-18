import os
import yaml

from flask import Flask, jsonify, render_template, request
from flask_swaggerui import render_swaggerui, build_static_blueprint
from search import Search

app = Flask(__name__)
app.register_blueprint(build_static_blueprint("swaggerui", __name__))


@app.route("/")
def index():
    """
    Root server page
    :return: Root server page
    """
    return render_template("search.html")


@app.route("/api/search/v1/search", methods=['GET'])
def search():
    """
    Returns a JSON response containing the results of the search term
    :return: JSON Response
    """
    term = request.args.get('q')
    limit = request.args.get('limit')
    if limit is None:
        limit = 20

    result = Search.search(term, limit)
    return jsonify(result)


@app.route("/api/search/v1/docs")
def search_docs():
    return render_swaggerui(swagger_spec_path="/api/search/v1/swagger")


@app.route("/api/search/v1/swagger")
def search_swagger():
    v1_swag = open(os.path.dirname(__file__) +
                   "/swagger/search.v1.swagger.yaml", "r")
    docs = yaml.load(v1_swag)
    return jsonify(docs)


@app.route("/api/validator/v1/docs")
def validator_docs():
    return render_swaggerui(swagger_spec_path="/api/validator/v1/swagger")


@app.route("/api/validator/v1/swagger")
def validator_swagger():
    v1_swag = open(os.path.dirname(__file__) +
                   "/swagger/validator.v1.swagger.yaml", "r")
    docs = yaml.load(v1_swag)
    return jsonify(docs)


@app.route("/api/validator/v1/validate", methods=['POST'])
def validate():
    stubObj = {
        "corporation": {
            "errors": [
                {
                    "code": 1,
                    "message": "Test Corp error",
                    "severity": 1
                }
            ],
            "valid": True,
            "value": "Ltd."
        },
        "descriptive": {
            "errors": [
                  {
                      "code": 1,
                      "message": "Test descriptive error",
                      "severity": 1
                  }
              ],
            "exists": True,
            "value": "Lawnmower"
        },
        "distinct": {
            "errors": [
                {
                    "code": 1,
                    "message": "Test distinctive error",
                    "severity": 1
                }
            ],
            "exists": True,
            "value": "Bob's"
        }
    }
    return jsonify(stubObj)

if __name__ == "__main__":
    app.run()
