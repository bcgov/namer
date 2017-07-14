import sys

from flask import Flask, jsonify, render_template, request
from search import Search

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("search.html")


@app.route("/api/v1.0/search", methods=['GET'])
def search():
    term = request.args.get('term')
    limit = request.args.get('limit')
    hits = list()

    if term not in (None, ''):
        term = term.upper()
        results = Search.search(term)
        names = Search.gather_names(results, term)

        if limit in (None, ''):
            limit = sys.maxsize
        for i, name in zip(range(int(limit)), names):
            hits.append({'id': str(i), 'label': name, 'value': name})

    return jsonify({'hits': hits})

if __name__ == "__main__":
    app.run()
