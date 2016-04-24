from crypto import paillier

class Authority:
    def __init__(self):
        self.keys = []

    def create_election(n_voters, n_candidates):
        self.keys.append(pallier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1].pk, len(self.keys) - 1)

    def compute_result(election_id, tallier):
        c = tallier.tally_votes()
        return pallier.decrypt(self.keys[election_id].pk, self.keys[election_id].sk, c)

class Election:
    def __init__(self, n_voters, n_candidates, pk, election_id):
        self.n_voters = n_voters
        self.n_candidates = n_candidates
        self.pk = pk
        self.election_id = election_id

if __name__ == '__main__':
    pk,sk = paillier.gen_keys()
    print(pk.n)
    print(pk.g)
    print(sk.l)
    print(sk.mu)
