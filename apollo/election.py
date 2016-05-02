class Election:
    def __init__(self, voter_ids, candidates, owner, pk, election_id):
        self.voter_ids = voter_ids
        self.candidates = candidates
        self.owner = owner
        self.n_voters = len(voter_ids)
        self.n_candidates = len(candidates)
        self.pk = pk
        self.election_id = election_id

        assert pow(self.n_voters, self.n_candidates) < self.pk.n

    def decode_result(self, result):
        m = self.n_voters + 1
        vote_totals = {self.candidates[i]:0 for i in range(self.n_candidates)}

        i = 0
        while result != 0:
            vote_totals[self.candidates[i]] = (result % m)
            result = result // m
            i += 1

        return vote_totals
