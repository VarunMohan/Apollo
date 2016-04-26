from client_authority import ClientAuthority
from client_aggregate_tallier import ClientAggregateTallier
from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
import entity_locations
import sys
from voter import Voter

import pickle
from flask import Flask, render_template, request
from flaskext.xmlrpc import XMLRPCHandler, Fault

class Registrar:
    def __init__(self, endpoint):
        self.table = {}
        self.endpoint = endpoint
        self.tallier_endpoints = []

    def register_election(self, voter_ids, candidates):
        n_voters = len(voter_ids)
        n_candidates = len(candidates)
        a = ClientAuthority()
        election = a.create_election(voter_ids, candidates)
        election_talliers = []
        for endpoint in self.tallier_endpoints:
            tallier = ClientTallier(endpoint)
            if (tallier.request_election(election, self.endpoint)):
                election_talliers.append(endpoint)
                # random threshold
                if ((n_candidates * n_voters)/(len(election_talliers)) < 100):
                    break
        if len(election_talliers) == 0:
            print('Failed to Register Election ID: ' + str(election.election_id))
            return False
        aggregate_tallier = ClientAggregateTallier()
        aggregate_tallier.register_talliers(election.election_id, election_talliers, self.endpoint, election.pk)
        self.table[election.election_id] = TableEntry(election, election_talliers, False)
        print('Registered Election ID: ' + str(election.election_id))
        sys.stdout.flush()
        return election.election_id

    def register_tallier(self, endpoint):
        print('Registered Tallier:', endpoint.hostname, str(endpoint.port))
        self.tallier_endpoints.append(endpoint)
        return True

    def get_election(self, election_id):
        return self.table[election_id].election, self.table[election_id].tallier_endpoints

    def add_voter(self, election_id, voter_id, vote):
        if election_id not in self.table or voter_id in self.table[election_id].registrar:
            return False
        if self.table[election_id].done:
            return False
        record = VoterRecord(vote, False)
        self.table[election_id].registrar[voter_id] = record
        return True

    def confirm_vote(self, election_id, voter_id, vote):
        if election_id not in self.table or voter_id not in self.table[election_id].registrar:
            return False
        if self.table[election_id].done:
            return False
        record = self.table[election_id].registrar[voter_id]
        if record.has_voted or record.vote != vote:
            return False
        record.has_voted = True
        return True

    def voting_complete(self, election_id):
        print("Voting Complete for Election", election_id)
        # will add a publish feature after this
        if election_id not in self.table or self.table[election_id].done:
            return False
        self.table[election_id].done = True
        return True

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
endpoint = entity_locations.get_registrar_endpoint()
r = Registrar(endpoint)

@handler.register
def register_election(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.register_election(args['voter_ids'], args['candidates']))

@handler.register
def register_tallier(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.register_tallier(args['endpoint']))

# May need an unregister command

@handler.register
def get_election(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.get_election(args['election_id']))

@handler.register
def add_voter(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.add_voter(args['election_id'], args['voter_id'], args['vote']))

@handler.register
def confirm_vote(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.confirm_vote(args['election_id'], args['voter_id'], args['vote']))

@handler.register
def voting_complete(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.voting_complete(args['election_id']))

@app.route('/')
def hello_world():
    return render_template('registrar.html')

class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted

class TableEntry:
    def __init__(self, election, tallier_endpoints, done):
        self.election = election
        self.tallier_endpoints = tallier_endpoints
        self.registrar = {}
        self.done = False

if __name__ == '__main__':
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

