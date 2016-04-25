from registrar import Registrar
from crypto import paillier

import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
import sys

class Tallier:
    def __init__(self, registrar, election):
        # self.registrar = registrar
        self.election = election
        self.vote_tally = 1
        self.tallied = False

    def send_vote(self, voter_id, vote):
        if self.registrar.confirm_vote(voter_id, vote):
            self.vote_tally = paillier.add(self.election.pk, self.vote_tally, vote)
            return True
        return False

    def send_vote(self, voter_id, vote, registrar):
        if registrar.confirm_vote(voter_id, vote):
            self.vote_tally = paillier.add(self.election.pk, self.vote_tally, vote)
            return True
        return False

    def tally_votes(self, election_id):
        if self.election.election_id != election_id:
            return False
        # dumb fix
        # self.registrar.voting_complete()
        if not self.tallied:
            return self.vote_tally
        else:
            return False

class ServerTallier:
    def __init__(self):
        self.t = Tallier()

    def send_vote(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.send_vote(args['voter_id'], args['vote']))

    def tally_votes(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.t.tally_votes(args['election_id']))

class ClientTallier:
    def __init__(self, port):
        self.t = xmlrpc.client.ServerProxy("http://localhost:" + str(port) + "/")

    def send_vote(self, voter_id, vote):
        args = {'voter_id': voter_id, 'vote': vote}
        resp = self.t.send_vote(pickle.dumps(args))
        return pickle.loads(resp.data)

    def tally_votes(self, election_id):
        args = {'election_id': election_id}
        resp = self.t.tally_votes(pickle.dumps(args))
        return pickle.loads(resp.data)

if __name__ == '__main__':
    assert(len(sys.argv) == 2)
    tallier = ServerTallier()
    server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])))
    print("Listening on port " + sys.argv[1] + "...")
    server.register_function(tallier.send_vote, "send_vote")
    server.register_function(tallier.tally_votes, "tally_votes")
    server.serve_forever()
