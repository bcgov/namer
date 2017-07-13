import json

from flask import Flask, render_template, request
from search import Search

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("search.html")


@app.route("/search")
def search():
    term = request.args.get('term', '')
    results = Search.search(term.upper())
    names = Search.gather_names(results)

    hits = list()
    for i, name in enumerate(names):
        hit = {'id': term[0].upper() + term[1::] + str(i),
               'label': name,
               'value': name}
        hits.append(hit)

    return json.dumps(hits)

if __name__ == "__main__":
    app.run()
