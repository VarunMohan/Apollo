from crypto import paillier, znp
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
        self.ciphers = []
        self.endpoint = endpoint

    def create_election(self):
        self.keys.append(paillier.gen_keys())
        self.election_running.append(True)
        self.results.append(None)
        self.ciphers.append(None) 
        return (self.keys[-1][0], len(self.keys))
        # return Election(voter_ids, candidates, self.keys[-1][0], len(self.keys))

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
        self.ciphers[election_id - 1] = c
        return result

    def verify_election(self, election_id, e_chall):
        pk, sk  = self.keys[election_id - 1]
        if self.results[election_id - 1] == None:
            return False
        print(pk, sk, self.ciphers[election_id - 1], e_chall)
        sys.stdout.flush()
        return znp.decrypt_proof(pk, sk, self.ciphers[election_id - 1], e_chall) 

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
endpoint = entity_locations.get_authority_endpoint()
a = Authority(endpoint)

@handler.register
def create_election():
    return pickle.dumps(a.create_election())

@handler.register
def compute_result(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.compute_result(args['election_id']))

@handler.register
def verify_election(req):
    args = pickle.loads(req.data)
    print(args)
    sys.stdout.flush()
    return pickle.dumps(a.verify_election(args['election_id'], args['e_chall']))

if __name__ == '__main__':
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)
