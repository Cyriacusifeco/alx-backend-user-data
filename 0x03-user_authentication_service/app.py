#!/usr/bin/env python3
"""
Simple flask app
"""

from flask import Flask, request, jsonify, make_response, abort
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/")
def welcome():
    """
    Simple welcome
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Register new users
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    User login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return make_response(
                jsonify({"error": "Missing email or password"}),
                400
                )

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id:
            response = make_response(
                    jsonify({"email": email, "message": "logged in"}),
                    200
                    )
            response.set_cookie('session_id', session_id)
            return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
