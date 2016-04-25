from clientregistrar import ClientRegistrar
from crypto import paillier, znp
import entitylocations
import sys

import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
import pickle

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

class ServerTallier:
    def __init__(self):
        self.t = Tallier()

    def request_election(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.request_election(args['election'], args['r_endpoint']))

    def send_vote(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.send_vote(args['voter_id'], args['vote'], args['proof']))

    def tally_votes(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.tally_votes(args['election_id']))

if __name__ == '__main__':
    tallier = ServerTallier()
    assert(len(sys.argv) == 2)
    endpoint = entitylocations.get_tallier_endpoints()[int(sys.argv[1])]
    server = SimpleXMLRPCServer((endpoint.hostname, endpoint.port))
    server.register_function(tallier.request_election, "request_election")
    server.register_function(tallier.send_vote, "send_vote")
    server.register_function(tallier.tally_votes, "tally_votes")
    server.serve_forever()
