#!/usr/bin/env python3
"""Simple Flask web application.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    """Root route handler.
    """
    return jsonify({
        "message": "Bienvenue"
        })


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Registration users endpoint
    """
    try:
        user = AUTH.register_user(
                request.form.get("email"),
                request.form.get("password")
                )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Login endpoint
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
    else:
        abort(401)

    return jsonify({
        "email": email, "message": "logged in"
        }).set_cookie("session_id", session_id)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """ """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
