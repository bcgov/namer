from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/test")
def test():
    return render_template("search.html")

@app.route("/search")
def search():

    term = request.args.get('term', '')
    hits = []

    for i in range(3):
        hit = {}
        hit['id'] = term[0].upper() + term[1::] + str(i)
        hit['label'] = term[0].upper() + term[1::] + str(i) + " label"
        hit['value'] = term[0].upper() + term[1::] + str(i) + " value"
        hits.append(hit)

    return json.dumps(hits)

if __name__ == "__main__":
    app.run()
