from crypto import paillier
from election import Election
from clienttallier import ClientTallier

import pickle
import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer

class Authority:
    def __init__(self):
        self.keys = []

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys) - 1)

    def compute_result(self, election_id):
        tallier = ClientTallier()
        c = tallier.tally_votes(election_id)
        if not c:
            return False
        return paillier.decrypt(self.keys[election_id][0], self.keys[election_id][1], c)

class ServerAuthority:
    def __init__(self):
        self.a = Authority()

    def create_election(self, req):
        args = pickle.loads(req.data) 
        return pickle.dumps(self.a.create_election(args['n_voters'], args['n_candidates']))

    def compute_result(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.a.compute_result(args['election_id']))


if __name__ == '__main__':
    authority = ServerAuthority()
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(authority.create_election, "create_election")
    server.register_function(authority.compute_result, "compute_result")
    server.serve_forever()
