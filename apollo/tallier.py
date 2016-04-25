from clientregistrar import ClientRegistrar
from crypto import paillier

import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
import pickle

class Tallier:
    def __init__(self):
        self.election = None
        self.registrar = ClientRegistrar()
        self.vote_tally = 1
        self.tallied = True

    # def __init__(self, registrar, election):
        # # self.registrar = registrar
        # self.election = election
        # self.vote_tally = 1
        # self.tallied = False

    def request_election(self, election):
        if not self.tallied:
            return False

        self.election = election
        self.tallied = False
        return True

    def send_vote(self, voter_id, vote):
        if self.registrar.confirm_vote(voter_id, vote):
            self.vote_tally = paillier.add(self.election.pk, self.vote_tally, vote)
            # print(self.vote_tally)
            return True
        return False

    def tally_votes(self, election_id):
        if self.election.election_id != election_id:
            return False
        # dumb fix
        self.registrar.voting_complete()
        if not self.tallied:
            return self.vote_tally
        else:
            return False

class ServerTallier:
    def __init__(self):
        self.t = Tallier()

    def request_election(self, req):
        args = pickle.loads(req.data)
        print(args)
        return pickle.dumps(self.t.request_election(args['election']))

    def send_vote(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.send_vote(args['voter_id'], args['vote']))

    def tally_votes(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.tally_votes(args['election_id']))

if __name__ == '__main__':
    tallier = ServerTallier()
    server = SimpleXMLRPCServer(("localhost", 9001))
    print("Listening on port 9001...")
    server.register_function(tallier.request_election, "request_election")
    server.register_function(tallier.send_vote, "send_vote")
    server.register_function(tallier.tally_votes, "tally_votes")
    server.serve_forever()
