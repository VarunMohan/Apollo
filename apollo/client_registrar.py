import pickle
import sys
import xmlrpc.client

class ClientRegistrar:
    def __init__(self, endpoint):
        url = 'http://' + endpoint.hostname + ':' + str(endpoint.port) + '/api'
        print('Channel With Registrar: ' + url)
        sys.stdout.flush()
        self.r = xmlrpc.client.ServerProxy(url)

    def register_election(self, voter_ids, candidates):
        args = {'voter_ids': voter_ids, 'candidates': candidates}
        resp = self.r.register_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def register_tallier(self, endpoint):
        args = {'endpoint': endpoint}
        resp = self.r.register_tallier(pickle.dumps(args))
        return pickle.loads(resp.data)

    def get_election(self, election_id):
        args = {'election_id': election_id}
        resp = self.r.get_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def list_election_ids(self):
        resp = self.r.list_election_ids()
        return pickle.loads(resp.data)

    def end_election(self, election_id):
        args = {'election_id': election_id}
        resp = self.r.end_election(pickle.dumps(args))
        return pickle.loads(resp.data)

    def is_election_running(self, election_id):
        args = {'election_id': election_id}
        resp = self.r.is_election_running(pickle.dumps(args))
        return pickle.loads(resp.data)

    def get_result(self, election_id):
        args = {'election_id': election_id}
        resp = self.r.get_result(pickle.dumps(args))
        return pickle.loads(resp.data)

    def add_voter(self, election_id, voter_id, vote):
        args = {'election_id': election_id, 'voter_id': voter_id, 'vote': vote}
        resp = self.r.add_voter(pickle.dumps(args))
        return pickle.loads(resp.data)

    def confirm_vote(self, election_id, voter_id, vote):
        args = {'election_id': election_id, 'voter_id': voter_id, 'vote': vote}
        resp = self.r.confirm_vote(pickle.dumps(args))
        return pickle.loads(resp.data)
