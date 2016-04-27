from client_registrar import ClientRegistrar
from crypto import paillier, znp
import entity_locations
import sys

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from flask import render_template
import sys

class Tallier:
    #Note, should handle multiple votes at the same time
    def __init__(self, tallier_id, endpoint, r_endpoint, num_elections):
        self.registrar = ClientRegistrar(r_endpoint)
        self.registrar.register_tallier(endpoint)
        print("Sent Registration Request")
        sys.stdout.flush()
        self.endpoint = endpoint
        self.vote_tallies = {}
        self.tallier_id = tallier_id
        self.num_elections = num_elections

    def request_election(self, election, r_endpoint):
        if len(self.vote_tallies) >= self.num_elections or election.election_id in self.vote_tallies:
            return False
        self.vote_tallies[election.election_id] = TallyRecord(election, 1)
        return True

    def send_vote(self, voter_id, election_id, vote, proof):
        if election_id not in self.vote_tallies:
            return False
        if self.registrar.confirm_vote(election_id, voter_id, vote):
            # zero-knowledge proof
            (u, a, e, z, esum) = proof
            pk = self.vote_tallies[election_id].election.pk
            if znp.check_proof(pk, u, a, e, z, esum):
                self.vote_tallies[election_id].tally = paillier.add(pk, self.vote_tallies[election_id].tally, vote)
                return True
        return False

    def tally_votes(self, election_id):
        if election_id not in self.vote_tallies:
            return False
        tally = self.vote_tallies[election_id].tally
        del self.vote_tallies[election_id]
        return tally

class TallyRecord:
    def __init__(self, election, tally):
        self.election = election
        self.tally = tally

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
    return pickle.dumps(t.send_vote(args['voter_id'], args['election_id'], args['vote'], args['proof']))

@handler.register
def tally_votes(req):
    args = pickle.loads(req.data)
    return pickle.dumps(t.tally_votes(args['election_id']))

@app.route('/')
def hello_world():
    return render_template('tallier.html', tallier_id = t.tallier_id, tallied = t.tallied)

if __name__ == '__main__':
    assert(len(sys.argv) == 3)
    tallier_id = int(sys.argv[1])
    num_elections = int(sys.argv[2])
    endpoint = entity_locations.get_tallier_endpoints()[tallier_id]
    registrar_endpoint = entity_locations.get_registrar_endpoint()
    t = Tallier(tallier_id, endpoint, registrar_endpoint, num_elections)
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

