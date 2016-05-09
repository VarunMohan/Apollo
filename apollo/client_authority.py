import pickle
import xmlrpc.client
import entity_locations
import sys

class ClientAuthority:
    def __init__(self):
        endpoint = entity_locations.get_authority_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With Authority: ' + url)
        sys.stdout.flush()
        self.a = xmlrpc.client.ServerProxy(url)

    def create_election(self):
        resp = self.a.create_election()
        return pickle.loads(resp.data)

    def compute_result(self, election_id):
        args = {'election_id': election_id}
        resp = self.a.compute_result(pickle.dumps(args))
        return pickle.loads(resp.data)

    def verify_election(self, election_id, e_chall):
        args = {'election_id': election_id, 'e_chall': e_chall}
        resp = self.a.verify_election(pickle.dumps(args))
        return pickle.loads(resp.data)
