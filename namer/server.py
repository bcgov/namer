import logging

from flask import Flask, g, jsonify, render_template, request
from flask_swaggerui import render_swaggerui, build_static_blueprint
from search import Search
from validator import Validator

app = Flask(__name__)
app.register_blueprint(build_static_blueprint("swaggerui", __name__))

log = logging.getLogger(__name__)


def load_swagger_yaml(filename):
    """
    Loads the YAML filename specified
    :param filename: Filename string of swagger YAML
    :return: JSON of swagger YAML filename
    """
    import os
    import yaml

    path = os.path.join(os.path.dirname(__file__), 'swagger', filename)
    v1_swag = open(path, 'r')
    docs = yaml.load(v1_swag)
    return jsonify(docs)


@app.before_request
def before_request():
    from timeit import default_timer as timer

    g.request_start_time = timer()
    g.request_time = lambda: "%s" % (timer() - g.request_start_time)


@app.after_request
def after_request(response):
    log.debug('Rendered in %ss', g.request_time())
    return response


@app.route('/')
def index():
    """
    Root server page
    :return: Root server page
    """
    return render_template("search.html")


@app.route('/api/search/v1/docs/')
def search_docs():
    """
    Renders swagger documentation for search API
    :return: Swagger documentation for search API
    """
    return render_swaggerui(swagger_spec_path="/api/search/v1/swagger")


@app.route('/api/search/v1/swagger')
def search_swagger():
    """
    Loads swagger YAML file for search API
    :return: JSON of swagger YAML file for search API
    """
    return load_swagger_yaml('search.v1.swagger.yaml')


@app.route('/api/search/v1/search', methods=['GET'])
def search_search():
    """
    Returns a JSON response containing the results of the search term
    :return: JSON Response of search results
    """
    query = request.args.get('q')
    limit = request.args.get('limit')
    if limit in (None, ''):
        limit = 20
    synonym = request.args.get('synonym')
    if synonym in (None, ''):
        synonym = False

    result = Search.search(query, limit, synonym)
    return jsonify(result)


@app.route('/api/validator/v1/docs/')
def validator_docs():
    """
    Renders swagger documentation for validator API
    :return: Swagger documentation for search API
    """
    return render_swaggerui(swagger_spec_path="/api/validator/v1/swagger")


@app.route('/api/validator/v1/swagger')
def validator_swagger():
    """
    Loads swagger YAML file for validator API
    :return: JSON of swagger YAML file for validator API
    """
    return load_swagger_yaml('validator.v1.swagger.yaml')


@app.route('/api/validator/v1/blacklist', methods=['GET'])
def validator_blacklist():
    """
    Returns a JSON response containing the results of blacklist occurrences
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.blacklist(query)
    return jsonify(result)


@app.route('/api/validator/v1/corporate', methods=['GET'])
def validator_corporate():
    """
    Returns a JSON response containing the results of corporate validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.corporate(query)
    return jsonify(result)


@app.route('/api/validator/v1/descriptive', methods=['GET'])
def validator_descriptive():
    """
    Returns a JSON response containing the results of descriptive validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.descriptive(query)
    return jsonify(result)


@app.route('/api/validator/v1/distinctive', methods=['GET'])
def validator_distinctive():
    """
    Returns a JSON response containing the results of distinctive validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.distinctive(query)
    return jsonify(result)


@app.route('/api/validator/v1/greylist', methods=['GET'])
def validator_greylist():
    """
    Returns a JSON response containing the results of greylist occurrences
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.greylist(query)
    return jsonify(result)


@app.route('/api/validator/v1/validate', methods=['GET'])
def validator_validate():
    """
    Returns a JSON response containing the results of overall validation
    :return: JSON Response of validation results
    """
    query = request.args.get('q')

    result = Validator.validate(query)
    return jsonify(result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    app.run()
