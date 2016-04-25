from clientauthority import ClientAuthority
from clientaggregatetallier import ClientAggregateTallier
from clienttallier import ClientTallier
import entitylocations

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault

class Registrar:
    def __init__(self, n_voters, n_candidates, endpoint):
        self.table = {}
        self.done = False
        self.a = ClientAuthority()
        self.election = self.a.create_election(n_voters, n_candidates)
        self.endpoint = endpoint
        self.tallier_endpoints = []
        tallier_endpoints = entitylocations.get_tallier_endpoints()
        for endpoint in tallier_endpoints:
            tallier = ClientTallier(endpoint)
            if (tallier.request_election(self.election, self.endpoint)):
                self.tallier_endpoints.append(endpoint)
        aggregate_tallier = ClientAggregateTallier()
        aggregate_tallier.register_talliers(self.election.election_id, self.tallier_endpoints, self.endpoint, self.election.pk)

        print('Authority Election ID: ' + str(self.election.election_id))

    def get_election(self):
        return self.election, self.tallier_endpoints

    def add_voter(self, voter_id, vote):
        if voter_id in self.table or self.done:
            return False
        record = VoterRecord(vote, False)
        self.table[voter_id] = record
        return True

    def confirm_vote(self, voter_id, vote):
        record = self.table[voter_id]
        if record.has_voted or record.vote != vote:
            return False
        record.has_voted = True
        return True

    def voting_complete(self):
        print("Voting is Complete")
        # will add a publish feature after this
        self.done = True
        self.table = {}
        self.election = None
        # dummy return
        return True

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
n_voters = 5
n_candidates = 5
endpoint = entitylocations.get_registrar_endpoint()
r = Registrar(n_voters, n_candidates, endpoint)


@handler.register
def get_election():
    return pickle.dumps(r.get_election())

@handler.register
def add_voter(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.add_voter(args['voter_id'], args['vote']))

@handler.register
def confirm_vote(req):
    args = pickle.loads(req.data)
    return pickle.dumps(r.confirm_vote(args['voter_id'], args['vote']))

@handler.register
def voting_complete():
    return pickle.dumps(r.voting_complete())

@app.route('/')
def hello_world():
    return 'Hello World!\nThis is the Registrar'

class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted

if __name__ == '__main__':
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)

