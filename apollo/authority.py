from crypto import paillier
import xmlrpc
import pickle
from xmlrpc.server import SimpleXMLRPCServer

class Authority:
    def __init__(self):
        self.keys = []

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys) - 1)

    def compute_result(self, election_id, tallier):
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
        return pickle.dumps(self.a.compute_result(args['election_id'], args['tallier']))

    # def create_election(self, n_voters, n_candidates):
        # print("HI1")
        # e = self.a.create_election(n_voters, n_candidates)
        # s = pickle.dumps(e)
        # return s

    # def compute_result(self, election_id, tallier):
        # return pickle.dumps(self.a.compute_result(election_id, tallier))

class ClientAuthority:
    def __init__(self):
        self.a = xmlrpc.client.ServerProxy("http://localhost:8000/")

    def create_election(self, n_voters, n_candidates):
        args = {'n_voters': n_voters, 'n_candidates': n_candidates}
        resp = self.a.create_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def compute_result(self, election_id, tallier):
        args = {'election_id': election_id, 'tallier': tallier}
        resp = self.a.compute_result(pickle.dumps(args)) 
        return pickle.loads(resp.data)

    # def compute_result(self, election_id, tallier):
        # return pickle.loads(self.a.compute_result(election_id, tallier).data)

class Election:
    def __init__(self, n_voters, n_candidates, pk, election_id):
        self.n_voters = n_voters
        self.n_candidates = n_candidates
        self.pk = pk
        self.election_id = election_id

        assert pow(n_voters, n_candidates) < self.pk.n

    def decode_result(self, result):
        m = self.n_voters
        vote_totals = {i:0 for i in range(self.n_candidates)}

        i = 0
        while result != 0:
            vote_totals[i] = (result % m)
            result = result // m
            i += 1

        return vote_totals

if __name__ == '__main__':
    # authority = Authority()
    authority = ServerAuthority()
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(authority.create_election, "create_election")
    server.register_function(authority.compute_result, "compute_result")
    server.serve_forever()
