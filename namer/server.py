import os
import yaml

from flask import Flask, jsonify, render_template, request
from flask_swaggerui import render_swaggerui, build_static_blueprint
from search import Search
from validator import Validate

app = Flask(__name__)
app.register_blueprint(build_static_blueprint("swaggerui", __name__))


@app.route("/")
def index():
    """
    Root server page
    :return: Root server page
    """
    return render_template("search.html")


@app.route("/api/search/v1/docs")
def search_docs():
    """
    Renders swagger documentation for search API
    :return: Swagger documentation for search API
    """
    return render_swaggerui(swagger_spec_path="/api/search/v1/swagger")


@app.route("/api/search/v1/swagger")
def search_swagger():
    """
    Loads swagger YAML file for search API
    :return: JSON of swagger YAML file for search API
    """
    v1_swag = open(os.path.dirname(__file__) +
                   "/swagger/search.v1.swagger.yaml", "r")
    docs = yaml.load(v1_swag)
    return jsonify(docs)


@app.route("/api/search/v1/search", methods=['GET'])
def search_search():
    """
    Returns a JSON response containing the results of the search term
    :return: JSON Response of search results
    """
    query = request.args.get('q')
    limit = request.args.get('limit')
    if limit is None:
        limit = 20

    result = Search.search(query, limit)
    return jsonify(result)


@app.route("/api/validator/v1/docs")
def validator_docs():
    """
    Renders swagger documentation for validator API
    :return: Swagger documentation for search API
    """
    return render_swaggerui(swagger_spec_path="/api/validator/v1/swagger")


@app.route("/api/validator/v1/swagger")
def validator_swagger():
    """
        Loads swagger YAML file for validator API
        :return: JSON of swagger YAML file for validator API
        """
    v1_swag = open(os.path.dirname(__file__) +
                   "/swagger/validator.v1.swagger.yaml", "r")
    docs = yaml.load(v1_swag)
    return jsonify(docs)


@app.route("/api/validator/v1/corporate", methods=['GET'])
def validator_corporate():
    """
    Returns a JSON response containing the results of corporate validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validate.corporate(query)
    return jsonify(result)


@app.route("/api/validator/v1/validate", methods=['GET'])
def validator_validate():
    """
    Returns a JSON response containing the results of overall validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validate.validate(query)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
