import xmlrpc
import pickle
import entitylocations
from clientauthority import ClientAuthority
from clienttallier import ClientTallier
from xmlrpc.server import SimpleXMLRPCServer

class Registrar:
    def __init__(self, n_voters, n_candidates):
        self.table = {}
        self.done = False
        self.a = ClientAuthority()
        self.election = self.a.create_election(n_voters, n_candidates)
        self.t = ClientTallier() 
        # for now assert
        assert(self.t.request_election(self.election))
        print('Authority Election ID: ' + str(self.election.election_id))

    def get_election(self):
        return self.election

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
        self.done = True
        self.table = {}
        self.election = None
        # dummy return
        return True

class ServerRegistrar:
    def __init__(self, n_voters, n_candidates):
        self.r = Registrar(n_voters, n_candidates)

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
    registrar = ServerRegistrar(50, 10)
    endpoint = entitylocations.get_registrar_endpoint()
    server = SimpleXMLRPCServer((endpoint.hostname, endpoint.port))
    # server = SimpleXMLRPCServer(("localhost", 7000))
    # print("Listening on port 7000...")
    server.register_function(registrar.get_election, "get_election")
    server.register_function(registrar.add_voter, "add_voter")
    server.register_function(registrar.confirm_vote, "confirm_vote")
    server.register_function(registrar.voting_complete,"voting_complete")
    server.serve_forever()
