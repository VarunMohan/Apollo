import xmlrpc
import pickle

class ClientTallier:
    def __init__(self):
        self.t = xmlrpc.client.ServerProxy("http://localhost:9002/")

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

