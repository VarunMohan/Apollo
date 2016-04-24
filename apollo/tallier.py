from registrar import Registrar

class Tallier:
    def __init__(self):
        self.registar = Registrar()
        self.vote_tally = 0
        self.tallied = False
    
    def send_vote(self, voter_id, vote):
        self.registrar.add_voter(voter_id, vote)
        self.vote_tally += vote
    
    def tally_votes(self):
        if not tallied:
            return self.vote_tally
        else:
            return 0