import pickle
import xmlrpc
import entitylocations

class ClientAuthority:
    def __init__(self):
        endpoint = entitylocations.get_authority_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With Authority: ' + url)
        self.a = xmlrpc.client.ServerProxy(url)

    def create_election(self, n_voters, n_candidates):
        args = {'n_voters': n_voters, 'n_candidates': n_candidates}
        resp = self.a.create_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def compute_result(self, election_id, tallier):
        args = {'election_id': election_id}
        resp = self.a.compute_result(pickle.dumps(args))
        return pickle.loads(resp.data)
