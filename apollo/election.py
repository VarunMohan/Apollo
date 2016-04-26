
class Election:
    def __init__(self, n_voters, n_candidates, pk, election_id):
        self.n_voters = n_voters
        self.n_candidates = n_candidates
        self.pk = pk
        self.election_id = election_id

        assert pow(n_voters, n_candidates) < self.pk.n

    def decode_result(self, result):
        m = self.n_voters + 1
        vote_totals = {i:0 for i in range(self.n_candidates)}

        i = 0
        while result != 0:
            vote_totals[i] = (result % m)
            result = result // m
            i += 1

        return vote_totals
