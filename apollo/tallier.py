from registrar import Registrar
from crypto import paillier

class Tallier:
    def __init__(self, registrar, election):
        self.registrar = registrar
        self.election = election
        self.vote_tally = 1
        self.tallied = False

    def send_vote(self, voter_id, vote):
        if self.registrar.confirm_vote(voter_id, vote):
            self.vote_tally = paillier.add(self.election.pk, self.vote_tally, vote)
            return True
        print("sexy")
        return False

    def tally_votes(self, election_id):
        if self.election.election_id != election_id:
            return False
        self.registrar.voting_complete()
        if not self.tallied:
            return self.vote_tally
        else:
            return False
