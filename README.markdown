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

When using an application factory this extension can be initialized by the `init_app()` function.

The following Flask Configs are automatically used by `init_app()`:

|Variable Name | Description |
|---|---|
|`ARGON2_TIME_COST`|Defines the amount of computation realized and therefore the execution time, given in number of iterations.|
|`ARGON2_MEMORY_COST`|Defines the memory usage, given in kibibytes.|
|`ARGON2_PARALLELISM`|Defines the number of parallel threads (changes the resulting hash value).|
|`ARGON2_HASH_LENGTH`|Length of the hash in bytes.|
|`ARGON2_SALT_LENGTH`|Length of random salt to be generated for each password.|
|`ARGON2_ENCODING`|The Argon2 C library expects bytes. So if hash() or verify() are passed an unicode string, it will be encoded using this encoding.|
The default values are the same as the [argon2_cffi library](https://argon2-cffi.readthedocs.io/en/stable/api.html#argon2.PasswordHasher).

Two primary methods are now exposed by way of the argon2 object. Use
them like so:

    pw_hash = argon2.generate_password_hash('secret_password')
    argon2.check_password_hash(pw_hash, 'secret_password')
