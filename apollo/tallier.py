from client_registrar import ClientRegistrar
from crypto import paillier, znp
import entity_locations
import sys

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault

class Tallier:
    def __init__(self):
        self.election = None
        # Shouldn't be done here, given during request election
        self.registrar = None
        # self.registrar = ClientRegistrar()
        self.tallied = True
        self.vote_tally = 1

    def request_election(self, election, r_endpoint):
        if not self.tallied:
            return False

        self.election = election
        self.registrar = ClientRegistrar(r_endpoint)
        self.tallied = False
        self.vote_tally = 1
        return True

    def send_vote(self, voter_id, vote, proof):
        if self.registrar.confirm_vote(voter_id, vote):
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
        # self.registrar.voting_complete()
        if not self.tallied:
            self.tallied = True
            return self.vote_tally
        else:
            return False

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
t = Tallier()

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
    return 'Hello World!\nThis is the Tallier'

if __name__ == '__main__':
    endpoint = entity_locations.get_tallier_endpoints()[int(sys.argv[1])]
    assert(len(sys.argv) == 2)
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)
