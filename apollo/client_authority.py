import pickle
import xmlrpc.client
import entity_locations

class ClientAuthority:
    def __init__(self):
        endpoint = entity_locations.get_authority_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With Authority: ' + url)
        self.a = xmlrpc.client.ServerProxy(url)

    def create_election(self):
        resp = self.a.create_election()
        return pickle.loads(resp.data)

    #will need prove result

    def compute_result(self, election_id):
        # this is soley for the sake of 'offline_runthrough.py'
        args = {'election_id': election_id}
        resp = self.a.compute_result(pickle.dumps(args))
        return pickle.loads(resp.data)
