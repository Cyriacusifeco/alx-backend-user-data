#!/usr/bin/env python3
"""
Simple flask app
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():
    """
    Simple welcome
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
