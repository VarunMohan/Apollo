import pickle
import xmlrpc
import entitylocations

class ClientRegistrar:
    def __init__(self):
        endpoint = entitylocations.get_registrar_endpoint()
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/'
        print('Channel With Registrar: ' + url)
        self.r = xmlrpc.client.ServerProxy(url)

    def get_election(self):
        resp = self.r.get_election()
        return pickle.loads(resp.data)
    
    def add_voter(self, voter_id, vote):
        args = {'voter_id': voter_id, 'vote': vote}
        resp = self.r.add_voter(pickle.dumps(args))
        return pickle.loads(resp.data)
        
    def confirm_vote(self, voter_id, vote):
        args = {'voter_id': voter_id, 'vote': vote}
        resp = self.r.confirm_vote(pickle.dumps(args))
        return pickle.loads(resp.data)
    
    def voting_complete(self):
        resp = self.r.voting_complete()
        return pickle.loads(resp.data)
