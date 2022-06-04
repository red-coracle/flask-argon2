import flask
import pytest
from argon2.profiles import CHEAPEST

from flask_argon2 import Argon2, check_password_hash, generate_password_hash


@pytest.fixture(scope='module')
def _argon2():
    app = flask.Flask(__name__)
    return Argon2(app)


def test_check_hash(_argon2):
    pw_hash = _argon2.generate_password_hash('secret')
    assert check_password_hash(pw_hash, 'secret') is True
    pw_hash = _argon2.generate_password_hash(u'\u2603')
    assert _argon2.check_password_hash(pw_hash, u'\u2603') is True
    pw_hash = generate_password_hash('hunter2')
    assert check_password_hash(pw_hash, 'hunter2') is True


def test_unicode_hash(_argon2):
    password = u'東京'
    pw_hash = _argon2.generate_password_hash(password)
    assert _argon2.check_password_hash(pw_hash, password) is True


def test_hash_error(_argon2):
    pw_hash = _argon2.generate_password_hash('secret')
    assert _argon2.check_password_hash(pw_hash, 'hunter2') is False


def test_invalid_hash(_argon2):
    assert _argon2.check_password_hash('secret', 'hunter2') is False


def test_init_override():
    app = flask.Flask(__name__)
    _argon2 = Argon2(app, parallelism=3)
    pw_hash = _argon2.generate_password_hash('secret')
    assert _argon2.parallelism == 3
    assert _argon2.check_password_hash(pw_hash, 'secret') is True


def test_app_config_override():
    app = flask.Flask(__name__)
    app.config['ARGON2_MEMORY_COST'] = CHEAPEST.memory_cost
    _argon2 = Argon2(app)
    assert _argon2.memory_cost == CHEAPEST.memory_cost
    assert _argon2.ph.memory_cost == CHEAPEST.memory_cost


def test_multiple_overrides():
    app = flask.Flask(__name__)
    app.config['ARGON2_PARALLELISM'] = CHEAPEST.parallelism
    _argon2 = Argon2(app, hash_len=16)
    assert _argon2.parallelism == CHEAPEST.parallelism
    assert _argon2.hash_len == 16


def test_multiple_override_same_parameter():
    app = flask.Flask(__name__)
    app.config['ARGON2_PARALLELISM'] = CHEAPEST.parallelism
    _argon2 = Argon2(app, parallelism=8)
    assert _argon2.parallelism == CHEAPEST.parallelism
    assert _argon2.ph.parallelism == CHEAPEST.parallelism
