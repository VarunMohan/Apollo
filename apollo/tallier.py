from registrar import Registrar

class Tallier:
    def __init__(self, registrar):
        self.registrar = registrar
        self.vote_tally = 0
        self.tallied = False

    def send_vote(self, voter_id, vote):
        if self.registrar.add_voter(voter_id, vote):
            self.vote_tally += vote
            return True
        return False

    def tally_votes(self):
        if not self.tallied:
            return self.vote_tally
        else:
            return 0