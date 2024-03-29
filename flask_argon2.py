"""
    flaskext.argon2
    ---------------

    A Flask extension providing argon2 hashing and comparison.

    :copyright: (c) 2022 by red-coracle.
    :license: MIT, see LICENSE for more details.
"""


__version_info__ = ('0', '3', '0', '0')
__version__ = '.'.join(__version_info__)
__author__ = 'red-coracle'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 red-coracle'
__all__ = ['Argon2', 'generate_password_hash', 'check_password_hash']

try:
    import argon2
    from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
except ImportError as e:
    print('argon2_cffi is required to use Flask-Argon2')
    raise e


def generate_password_hash(password):
    '''
    This helper function wraps the identical method of :class:`Argon2`. It
    is intended to be used as a helper function at the expense of the
    configuration variable provided when passing back the app object. In other
    words, this shortcut does not make use of the app object at all.
    To use this function, simply import it from the module and use it in a
    similar fashion as using the method. Here is a quick example::
        from flask_argon2 import generate_password_hash
        pw_hash = generate_password_hash('hunter2')

    :param password: The password to be hashed.
    '''
    return Argon2().generate_password_hash(password)


def check_password_hash(pw_hash, password):
    '''
    This helper function wraps the similarly names method of :class:`Argon2.` It
    is intended to be used as a helper function at the expense of the
    configuration variable provided when passing back the app object. In other
    words, this shortcut does not make use of the app object at all.

    To use this function, simply import it from the module and use it in a
    similar fashion as using the method. Here is a quick example::

        from flask_argon2 import check_password_hash
        check_password_hash(pw_hash, 'hunter2') # returns True

    :param pw_hash: The hash to be compared against.
    :param password: The password to compare.
    '''
    return Argon2().check_password_hash(pw_hash, password)


class Argon2(object):
    '''
    Argon2 class container for password hashing and checking logic using
    argon2, of course. This class may be used to intialize your Flask app
    object. The purpose is to provide a simple interface for overriding
    Werkzeug's built-in password hashing utilities.
    Although such methods are not actually overriden, the API is intentionally
    made similar so that existing applications which make use of the previous
    hashing functions might be easily adapted to the stronger facility of
    argon2.
    To get started you will wrap your application's app object something like
    this::
        app = Flask(__name__)
        argon2 = Argon2(app)
    Now the two primary utility methods are exposed via this object, `argon2`.
    So in the context of the application, important data, such as passwords,
    could be hashed using this syntax::
        password = 'hunter2'
        pw_hash = argon2.generate_password_hash(password)
    Once hashed, the value is irreversible. However in the case of validating
    logins a simple hashing of candidate password and subsequent comparison.
    Importantly a comparison should be done in constant time. This helps
    prevent timing attacks. A simple utility method is provided for this::
        candidate = 'secret'
        argon2.check_password_hash(pw_hash, candidate)
    If both the candidate and the existing password hash are a match
    `check_password_hash` returns True. Otherwise, it returns False.
    .. admonition:: Namespacing Issues
        It's worth noting that if you use the format, `argon2 = Argon2(app)`
        you are effectively overriding the argon2 module. Though it's unlikely
        you would need to access the module outside of the scope of the
        extension be aware that it's overriden.
        Alternatively consider using a different name, such as `flask_argon2
        = Argon2(app)` to prevent naming collisions.
    :param app: The Flask application object. Defaults to None.
    '''

    _time_cost = argon2.DEFAULT_TIME_COST
    _memory_cost = argon2.DEFAULT_MEMORY_COST
    _parallelism = argon2.DEFAULT_PARALLELISM
    _hash_len = argon2.DEFAULT_HASH_LENGTH
    _salt_len = argon2.DEFAULT_RANDOM_SALT_LENGTH
    _encoding = 'utf-8'

    def __init__(self,
                 app=None,
                 time_cost: int = None,
                 memory_cost: int = None,
                 parallelism: int = None,
                 hash_len: int = None,
                 salt_len: int = None,
                 encoding: str = None):
        # Keep for backwards compatibility
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len
        self.encoding = encoding
        self.init_app(app)

    def init_app(self, app):
        '''Initalizes the application with the extension.
        :param app: The Flask application object.
        '''

        self.time_cost = self.time_cost or self._time_cost
        self.memory_cost = self.memory_cost or self._memory_cost
        self.parallelism = self.parallelism or self._parallelism
        self.hash_len = self.hash_len or self._hash_len
        self.salt_len = self.salt_len or self._salt_len
        self.encoding = self.encoding or self._encoding

        if app is not None:
            self.time_cost = app.config.get('ARGON2_TIME_COST', self.time_cost)
            self.memory_cost = app.config.get('ARGON2_MEMORY_COST', self.memory_cost)
            self.parallelism = app.config.get('ARGON2_PARALLELISM', self.parallelism)
            self.hash_len = app.config.get('ARGON2_HASH_LENGTH', self.hash_len)
            self.salt_len = app.config.get('ARGON2_SALT_LENGTH', self.salt_len)
            self.encoding = app.config.get('ARGON2_ENCODING', self.encoding)

        self.ph = argon2.PasswordHasher(self.time_cost,
                                        self.memory_cost,
                                        self.parallelism,
                                        self.hash_len,
                                        self.salt_len,
                                        self.encoding)

    def generate_password_hash(self, password):
        '''Generates a password hash using argon2.
        Example usage of :class:`generate_password_hash` might look something
        like this::
            pw_hash = argon2.generate_password_hash('secret')
        :param password: The password to be hashed.
        '''

        if not password:
            raise ValueError('Password must be non-empty.')

        return self.ph.hash(password)

    def check_password_hash(self, pw_hash, password):
        '''Tests a password hash against a candidate password. The candidate
        password is first hashed and then subsequently compared in constant
        time to the existing hash. This will either return `True` or `False`.
        Example usage of :class:`check_password_hash` would look something
        like this::
            pw_hash = argon2.generate_password_hash('secret')
            argon2.check_password_hash(pw_hash, 'secret') # returns True
        :param pw_hash: The hash to be compared against.
        :param password: The password to compare.
        '''

        try:
            return self.ph.verify(pw_hash, password)
        except VerifyMismatchError:
            return False
        except VerificationError:
            return False
        except InvalidHash:
            return False
