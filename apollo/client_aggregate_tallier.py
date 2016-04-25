import xmlrpc
import pickle
import entity_locations

class ClientAggregateTallier:
    def __init__(self):
        endpoint = entity_locations.get_aggregate_tallier_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With AggregateTallier: ' + url)
        self.t = xmlrpc.client.ServerProxy(url)

    def register_talliers(self, election_id, tallier_endpoints, registrar_endpoint, pk):
        args = {'election_id': election_id, 'tallier_endpoints': tallier_endpoints, 'registrar_endpoint': registrar_endpoint, 'pk': pk}
        resp = self.t.register_talliers(pickle.dumps(args))
        return pickle.loads(resp.data)

    def compute_aggregate_tally(self, election_id):
        args = {'election_id': election_id}
        resp = self.t.compute_aggregate_tally(pickle.dumps(args))
        return pickle.loads(resp.data)
