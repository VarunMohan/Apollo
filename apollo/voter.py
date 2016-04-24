class Voter:
    def __init__(self, voter_id, registrar, tallier):
        self.voter_id = voter_id
        self.registrar = registrar
        self.tallier = tallier

    def vote(self, vote):
        if self.registrar.add_voter(self.voter_id, vote):
            if self.tallier.send_vote(self.voter_id, vote):
                return True
        return False
