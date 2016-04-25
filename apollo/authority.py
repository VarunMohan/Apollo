from crypto import paillier
from election import Election
from clienttallier import ClientTallier
from clientaggregatetallier import ClientAggregateTallier
import entitylocations

import pickle
import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer

class Authority:
    def __init__(self, endpoint):
        self.keys = []
        self.endpoint = endpoint

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys) - 1)

    def compute_result(self, election_id):
        tallier = ClientAggregateTallier()
        c = tallier.compute_aggregate_tally(election_id) 
        if not c:
            return False
        return paillier.decrypt(self.keys[election_id][0], self.keys[election_id][1], c)

class ServerAuthority:
    def __init__(self, endpoint):
        self.a = Authority(endpoint)

    def create_election(self, req):
        args = pickle.loads(req.data) 
        return pickle.dumps(self.a.create_election(args['n_voters'], args['n_candidates']))

    def compute_result(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.a.compute_result(args['election_id']))


if __name__ == '__main__':
    endpoint = entitylocations.get_authority_endpoint()
    authority = ServerAuthority(endpoint)
    server = SimpleXMLRPCServer((endpoint.hostname, endpoint.port))
    server.register_function(authority.create_election, "create_election")
    server.register_function(authority.compute_result, "compute_result")
    server.serve_forever()
