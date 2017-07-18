from flask import Flask, jsonify, render_template, request
from search import Search

app = Flask(__name__)


@app.route("/")
def index():
    """
    Root server page
    :return: Root server page
    """
    return render_template("search.html")


@app.route("/api/v1/search", methods=['GET'])
def search():
    """
    Returns a JSON response containing the results of the search term
    :return: JSON Response
    """
    term = request.args.get('term')
    limit = request.args.get('limit')

    result = Search.search(term, limit)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
