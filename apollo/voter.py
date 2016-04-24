from registrar import Registrar

class Voter:
    def __init__(self, voter_id, registrar, tallier):
        self.voter_id = voter_id
        self.registrar = registrar
        self.tallier = tallier

    def vote(vote):
        if self.registrar.add_voter(voter_id, vote):
            if self.tallier.send_vote(voter_id, vote):
                return True
        return False
