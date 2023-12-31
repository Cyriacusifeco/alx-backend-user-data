#!/usr/bin/env python3
"""
Simple flask app
"""

from flask import Flask, request, jsonify, make_response, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logs a user out of an existing session
    """
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            response = redirect('/')
            response.delete_cookie('session_id')
            return response

    return jsonify(message="Forbidden"), 403


@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify(email=user.email), 200

    return jsonify(message="Forbidden"), 403


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Reset password
    """
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = {
            "email": email,
            "reset_token": reset_token
        }
        return jsonify(response), 200
    except ValueError:
        return "Forbidden", 403


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update password end-point
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except NoResultFound:
        return "", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
