from flask import request

import run as app
import unittest
import json
import os
from tests.test_data import InitData
from tests.expected_results.proposals import proposals


class AppTestCase(unittest.TestCase):
    def setUp(self):

        #print("==> Setting up a test environment ==>")

        app.app.config['TESTING'] = True

        self.app = app.app.test_client()

    def tearDown(self):
        print("<== Tearing down the test <==")
        # g.TESTING = False

    def test_graphql_methods(self):
        print("    >> Testing GraphQl Methods ==", end="")
        resp = self.app.get("/graphql")
        assert '400 BAD REQUEST' == resp.status

        resp = self.app.post("/graphql")
        assert '400 BAD REQUEST' == resp.status

        resp = self.app.put("/graphql")
        assert '405 METHOD NOT ALLOWED' == resp.status

        resp = self.app.delete("/graphql")
        assert '405 METHOD NOT ALLOWED' == resp.status

        resp = self.app.post('/graphql?query={proposals(semester:"2017-1"){proposalcode{ProposalCode}}}')
        assert '200 OK' == resp.status

        resp = self.app.get('/graphql?query={proposals(semester:"2017-1"){proposalcode{ProposalCode}}}')
        assert '200 OK' == resp.status

        print(" Passed << ")

    def test_graphql_results(self):
        print("    >> Testing GraphQl Results ==")
        resp = self.app.get('/graphql?query={proposals(semester:"2017-1"){proposalcode{ProposalCode}}}')
        # assert 1 == len(resp.response)

        resp = self.app.post('/graphql?query={proposals(semester:"2017-1"){proposalcode{ProposalCode}}}')
        data = json.loads(resp.get_data(as_text=True))

        self.assertEqual(len(data['data']['proposals']),
                         len(proposals['data']['proposals']))

        print(" Passed << ")

