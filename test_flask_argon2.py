# coding:utf-8

import unittest
import flask
from flask_argon2 import (Argon2, check_password_hash, generate_password_hash)


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        self.argon2 = Argon2(app)

    def test_check_hash(self):
        pw_hash = self.argon2.generate_password_hash('secret')
        self.assertTrue(self.argon2.check_password_hash(pw_hash, 'secret'))
        pw_hash = self.argon2.generate_password_hash(u'\u2603')
        self.assertTrue(self.argon2.check_password_hash(pw_hash, u'\u2603'))
        pw_hash = generate_password_hash('hunter2')
        self.assertTrue(check_password_hash(pw_hash, 'hunter2'))

    def test_unicode_hash(self):
        password = u'東京'
        pw_hash = generate_password_hash(password)
        self.assertTrue(check_password_hash(pw_hash, password))

    def test_hash_error(self):
        pw_hash = self.argon2.generate_password_hash('secret')
        self.assertFalse(self.argon2.check_password_hash(pw_hash, 'hunter2'))
    
    def test_hash_invalid_hash(self):
        """ Check that an InvalidHash is raised when an unhased password is used. """
        self.assertFalse(self.argon2.check_password_hash('secret', 'hunter2'))


class OverridesTestCase(unittest.TestCase):

    def setUp(self):
        app = flask.Flask(__name__)
        self.argon2 = Argon2(app, parallelism=3)

    def test_changed_parallelism(self):
        pw_hash = self.argon2.generate_password_hash('secret')
        self.assertTrue(self.argon2.parallelism == 3)
        self.assertTrue(self.argon2.check_password_hash(pw_hash, 'secret'))

if __name__ == '__main__':
    unittest.main()
