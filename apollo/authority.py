from crypto import paillier
from election import Election
from client_tallier import ClientTallier
from client_aggregate_tallier import ClientAggregateTallier
import entity_locations

import pickle
from flask import Flask, render_template, request
from flaskext.xmlrpc import XMLRPCHandler, Fault
import sys

class Authority:
    def __init__(self, endpoint):
        self.keys = []
        self.election_running = []
        self.results = []
        self.endpoint = endpoint

    def create_election(self, voter_ids, candidates):
        self.keys.append(paillier.gen_keys())
        self.election_running.append(True)
        self.results.append(None)
        return Election(voter_ids, candidates, self.keys[-1][0], len(self.keys))

    def compute_result(self, election_id):
        if not self.election_running[election_id - 1]:
            return False
        tallier = ClientAggregateTallier()
        c = tallier.compute_aggregate_tally(election_id)
        if not c:
            return False
        result = paillier.decrypt(self.keys[election_id - 1][0], self.keys[election_id - 1][1], c)
        self.election_running[election_id - 1] = False
        self.results[election_id - 1] = result
        return result

    def get_result(self, election_id):
        if self.election_running[election_id - 1]:
            return False
        return self.results[election_id - 1]

    def is_election_running(self, election_id):
        return self.election_running[election_id - 1]

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
endpoint = entity_locations.get_authority_endpoint()
a = Authority(endpoint)

@handler.register
def create_election(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.create_election(args['voter_ids'], args['candidates']))

@handler.register
def get_result(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.get_result(args['election_id']))

@handler.register
def is_election_running(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.is_election_running(args['election_id']))

@app.route('/api/compute_result', methods=['POST'])
def compute_result():
    a.compute_result(int(request.form['eid']))
    return render_template('authority.html')

@app.route('/')
def hello_world():
    return render_template('authority.html')

if __name__ == '__main__':
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)
