from clienttallier import ClientTallier
from clientregistrar import ClientRegistrar 
from crypto import paillier
import entitylocations

import xmlrpc
from xmlrpc.server import SimpleXMLRPCServer
import pickle


class AggregateTallier:
    def __init__(self):
        self.elections = {}

    # coming from registrar
    def register_talliers(self, election_id, tallier_endpoints, registrar_endpoint, pk):
        self.elections[election_id] = (tallier_endpoints, registrar_endpoint, pk)
        return True

    # coming from authority
    def compute_aggregate_tally(self, election_id):
        if election_id not in self.elections:
            return False
        total = 1
        tallier_endpoints, registrar_endpoint, pk = self.elections[election_id]
        print(tallier_endpoints)
        for endpoint in tallier_endpoints:
            t = ClientTallier(endpoint)
            local_tally = t.tally_votes(election_id)
            if (local_tally):
                total = paillier.add(pk, local_tally, total)

        r = ClientRegistrar(registrar_endpoint)
        r.voting_complete()
        # May want to delete entries from table
        return total

class ServerAggregateTallier:
    def __init__(self):
        self.at = AggregateTallier()

    def register_talliers(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.at.register_talliers(args['election_id'], args['tallier_endpoints'], args['registrar_endpoint'], args['pk']))

    def compute_aggregate_tally(self, req):
        args = pickle.loads(req.data)
        return pickle.dumps(self.at.compute_aggregate_tally(args['election_id']))

if __name__ == '__main__':
    tallier = ServerAggregateTallier()
    endpoint = entitylocations.get_aggregate_tallier_endpoint()
    server = SimpleXMLRPCServer((endpoint.hostname, endpoint.port))
    server.register_function(tallier.register_talliers, "register_talliers")
    server.register_function(tallier.compute_aggregate_tally, "compute_aggregate_tally")
    server.serve_forever()

