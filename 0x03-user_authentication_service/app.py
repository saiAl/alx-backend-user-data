#!/usr/bin/env python3
"""Simple Flask web application.
"""
from flask import Flask, jsonify, request
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
