from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("search.html")


@app.route("/search")
def search():
    term = request.args.get('term', '')
    hits = []

    for i in range(3):
        hit = {'id': term[0].upper() + term[1::] + str(i),
               'label': term[0].upper() + term[1::] + str(i) + " label",
               'value': term[0].upper() + term[1::] + str(i) + " value"}
        hits.append(hit)

    return json.dumps(hits)

if __name__ == "__main__":
    app.run()