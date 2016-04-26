from client_registrar import ClientRegistrar
from crypto import paillier, znp
import entity_locations
import sys

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from flask import render_template

class Tallier:
    #Note, should handle multiple votes at the same time
    def __init__(self, tallier_id, endpoint, r_endpoint):
        self.election = None
        self.registrar = ClientRegistrar(r_endpoint)
        self.registrar.register_tallier(endpoint)
        self.endpoint = endpoint
        self.tallied = True
        self.vote_tally = 1
        self.tallier_id = tallier_id

    def request_election(self, election, r_endpoint):
        if not self.tallied:
            return False

        self.election = election
        self.registrar = ClientRegistrar(r_endpoint)
        self.tallied = False
        self.vote_tally = 1
        return True

    def send_vote(self, voter_id, vote, proof):
        if self.registrar.confirm_vote(self.election.election_id, voter_id, vote):
            # zero-knowledge proof
            (u, a, e, z, esum) = proof
            if znp.check_proof(self.election.pk, u, a, e, z, esum):
                self.vote_tally = paillier.add(self.election.pk, self.vote_tally, vote)
                # print(self.vote_tally)
                return True
        print("vote failed")
        return False

    def tally_votes(self, election_id):
        if self.election.election_id != election_id:
            return False
        if not self.tallied:
            self.tallied = True
            return self.vote_tally
        else:
            return False

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
t = None

@handler.register
def request_election(req):
    args = pickle.loads(req.data)
    return pickle.dumps(t.request_election(args['election'], args['r_endpoint']))

@handler.register
def send_vote(req):
    args = pickle.loads(req.data)
    return pickle.dumps(t.send_vote(args['voter_id'], args['vote'], args['proof']))

@handler.register
def tally_votes(req):
    args = pickle.loads(req.data)
    return pickle.dumps(t.tally_votes(args['election_id']))

@app.route('/')
def hello_world():
    return render_template('tallier.html', tallier_id = t.tallier_id, tallied = t.tallied)

if __name__ == '__main__':
    assert(len(sys.argv) == 2)
    tallier_id = int(sys.argv[1])
    endpoint = entity_locations.get_tallier_endpoints()[tallier_id]
    registrar_endpoint = entity_locations.get_registrar_endpoint()
    # why do we pass tallier_id?
    t = Tallier(tallier_id, endpoint, registrar_endpoint)
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

