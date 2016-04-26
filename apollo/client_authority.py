import pickle
import xmlrpc.client
import entity_locations

class ClientAuthority:
    def __init__(self):
        endpoint = entity_locations.get_authority_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With Authority: ' + url)
        self.a = xmlrpc.client.ServerProxy(url)

    def create_election(self, voter_ids, candidates):
        args = {'voter_ids': voter_ids, 'candidates': candidates}
        resp = self.a.create_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def get_result(self, election_id):
        args = {'election_id': election_id}
        resp = self.a.get_result(pickle.dumps(args))
        return pickle.loads(resp.data)

    def is_election_running(self, election_id):
        args = {'election_id': election_id}
        resp = self.a.is_election_running(pickle.dumps(args))
        return pickle.loads(resp.data)
