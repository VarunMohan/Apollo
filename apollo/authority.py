from crypto import paillier

class Authority:
    def __init__(self):
        self.keys = []

    def create_election(self, n_voters, n_candidates):
        self.keys.append(paillier.gen_keys())
        return Election(n_voters, n_candidates, self.keys[-1][0], len(self.keys) - 1)

    def compute_result(self, election_id, tallier):
        c = tallier.tally_votes(election_id)
        if not c:
            return False
        return paillier.decrypt(self.keys[election_id][0], self.keys[election_id][1], c)

class Election:
    def __init__(self, n_voters, n_candidates, pk, election_id):
        self.n_voters = n_voters
        self.n_candidates = n_candidates
        self.pk = pk
        self.election_id = election_id

        assert pow(n_voters, n_candidates) < self.pk.n

    def decode_result(self, result):
        m = self.n_voters
        vote_totals = {i:0 for i in range(self.n_candidates)}

        i = 0
        while result != 0:
            vote_totals[i] = (result % m)
            result = result // m
            i += 1

        return vote_totals
