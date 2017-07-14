from flask import Flask, jsonify, render_template, request
from search import Search

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("search.html")


@app.route("/api/v1.0/search", methods=['GET'])
def search():
    term = request.args.get('term')
    hits = list()

    if term not in (None, ''):
        term = term.upper()
        results = Search.search(term)
        names = Search.gather_names(results, term)

        for i, name in enumerate(names):
            hits.append({'id': str(i), 'label': name, 'value': name})

    return jsonify({'hits': hits})

if __name__ == "__main__":
    app.run()
