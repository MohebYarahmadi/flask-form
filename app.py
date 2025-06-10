#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


app.run(debug=True, port=5001)
