from crypto import paillier
from election import Election
from client_tallier import ClientTallier
from client_aggregate_tallier import ClientAggregateTallier
import entity_locations

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from flask import render_template

class Authority:
    def __init__(self, endpoint):
        self.keys = []
        self.endpoint = endpoint

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys))

    def compute_result(self, election_id):
        tallier = ClientAggregateTallier()
        c = tallier.compute_aggregate_tally(election_id)
        if not c:
            return False
        return paillier.decrypt(self.keys[election_id - 1][0], self.keys[election_id - 1][1], c)

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
endpoint = entity_locations.get_authority_endpoint()
a = Authority(endpoint)

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
    return render_template('authority.html')

if __name__ == '__main__':
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)
