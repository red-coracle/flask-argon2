# Flask-Argon2

Flask-Argon2 is a Flask extension that provides Argon2 hashing utilities for
your Flask app.

## Installation

Install the extension with the following command:

    $ pip install flask-argon2

## Usage

To use the extension simply import the class wrapper and pass the Flask app
object back to here. Do so like this:

    from flask import Flask
    from flask_argon2 import Argon2

    app = Flask(__name__)
    argon2 = Argon2(app)

Two primary methods are now exposed by way of the argon2 object. Use
them like so:

    pw_hash = argon2.generate_password_hash('secret_password')
    argon2.check_password_hash(pw_hash, 'secret_password')
