import run as app
import unittest
import json
import os
from tests.test_data import InitData


class AppTestCase(unittest.TestCase):
    def setUp(self):

        print("==> Setting up a test environment ==>")

        app.app.config['TESTING'] = True
        InitData.test_user()

        self.app = app.app.test_client()

    def tearDown(self):
        print("<== Tearing down the test <==")
        # g.TESTING = False

    def test_token_methods(self):
        print("== Testing Token Methods ==")
        resp = self.app.get("/token")
        assert '405 METHOD NOT ALLOWED' == resp.status

        resp = self.app.put("/token")
        assert '405 METHOD NOT ALLOWED' == resp.status

        resp = self.app.delete("/token")
        assert '405 METHOD NOT ALLOWED' == resp.status

    def test_token_user(self):
        # Testing user validity
        print("== Testing Validity of a user ==")
        resp = self.app.post("/token")
        self.assertEquals({'error': 'username or password not provide'}, resp.status)
        resp = self.app.post("/token", data=json.dumps({'username': '', 'password': ''}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password not provide'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': 'test_user', 'password': ''}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password not provide'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': '', 'password': 'test123'}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password not provide'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': 'unknown_user', 'password': 'not_password'}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password incorrect'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': 'test_user', 'password': 'wrong_password'}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password incorrect'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': 'unknown_user', 'password': 'test123'}),
                             content_type='application/json')
        self.assertEquals({'error': 'username or password incorrect'}, resp.status)

        resp = self.app.post("/token", data=json.dumps({'username': 'test_user', 'password': 'test123'}),
                             content_type='application/json')
        self.assertEquals("200 OK", resp.status)

    def test_token(self):
        resp = self.app.get()