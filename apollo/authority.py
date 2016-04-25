from crypto import paillier
from election import Election
from clienttallier import ClientTallier
import entitylocations

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault

class Authority:
    def __init__(self):
        self.keys = []

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys) - 1)

    def compute_result(self, election_id):
        tallier = ClientTallier()
        c = tallier.tally_votes(election_id)
        if not c:
            return False
        return paillier.decrypt(self.keys[election_id][0], self.keys[election_id][1], c)

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
a = Authority()

@handler.register
def create_election(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.create_election(args['n_voters'], args['n_candidates']))

@handler.register
def compute_result(req):
    args = pickle.loads(req.data)
    return pickle.dumps(a.compute_result(args['election_id']))

@app.route('/')
def hello_world():
    return 'Hello World!\nThis is the Authority'

if __name__ == '__main__':
    endpoint = entitylocations.get_authority_endpoint()
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)
