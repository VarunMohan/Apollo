from crypto import paillier

class Voter:
    def __init__(self, voter_id, registrar, tallier, election):
        self.voter_id = voter_id
        self.registrar = registrar
        self.tallier = tallier
        self.election = election

    def encrypt_vote(self, candidate):
        m = self.election.n_voters
        vote = pow(m, candidate)
        return paillier.encrypt(self.election.pk, vote)

    def vote(self, candidate):
        encrypted_vote = self.encrypt_vote(candidate)
        if self.registrar.add_voter(self.voter_id, encrypted_vote):
            if self.tallier.send_vote(self.voter_id, encrypted_vote):
            # if self.tallier.send_vote(self.voter_id, encrypted_vote):
                return True
        return False
