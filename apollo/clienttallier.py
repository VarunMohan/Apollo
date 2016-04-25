import xmlrpc
import pickle
import entitylocations

class ClientTallier:
    def __init__(self):
        endpoint = entitylocations.get_tallier_endpoints()[0]
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/'
        print('Channel With Tallier: ' + url)
        self.t = xmlrpc.client.ServerProxy(url)
        # self.t = xmlrpc.client.ServerProxy("http://localhost:9002/")

    def request_election(self, election):
        args = {'election': election}
        resp = self.t.request_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def send_vote(self, voter_id, vote):
        args = {'voter_id': voter_id, 'vote': vote}
        resp = self.t.send_vote(pickle.dumps(args))
        return pickle.loads(resp.data)

    def tally_votes(self, election_id):
        args = {'election_id': election_id}
        resp = self.t.tally_votes(pickle.dumps(args))
        return pickle.loads(resp.data)

