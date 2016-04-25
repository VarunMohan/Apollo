import xmlrpc
import pickle
import entitylocations
from clientauthority import ClientAuthority
from clientaggregatetallier import ClientAggregateTallier
from clienttallier import ClientTallier
from xmlrpc.server import SimpleXMLRPCServer

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

class ServerRegistrar:
    def __init__(self, n_voters, n_candidates, endpoint):
        self.r = Registrar(n_voters, n_candidates, endpoint)

    def get_election(self):
        return pickle.dumps(self.r.get_election())
    
    def add_voter(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.r.add_voter(args['voter_id'], args['vote']))
    
    def confirm_vote(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.r.confirm_vote(args['voter_id'], args['vote']))
    
    def voting_complete(self):
        return pickle.dumps(self.r.voting_complete())

class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted

if __name__ == '__main__':
    endpoint = entitylocations.get_registrar_endpoint()
    registrar = ServerRegistrar(5, 5, endpoint)
    server = SimpleXMLRPCServer((endpoint.hostname, endpoint.port))
    server.register_function(registrar.get_election, "get_election")
    server.register_function(registrar.add_voter, "add_voter")
    server.register_function(registrar.confirm_vote, "confirm_vote")
    server.register_function(registrar.voting_complete,"voting_complete")
    server.serve_forever()
