from crypto import paillier
from crypto import znp
import Crypto.Util.number as pycrypto
import sys

class Voter:
    def __init__(self, voter_id, registrar, tallier, election):
        self.voter_id = voter_id
        self.registrar = registrar
        self.tallier = tallier
        self.election = election
        self.evote = None
        self.r = None
        self.proof = None

    def vote(self, evote, proof):
        self.evote = int(evote)
        self.proof = [list(map(int, proof[0])), list(map(int, proof[1])), list(map(int, proof[2])), list(map(int, proof[3])), int(proof[4])]
        if self.registrar.add_voter(self.election.election_id, self.voter_id, self.evote):
            if self.tallier.send_vote(self.voter_id, self.election.election_id, self.evote, self.proof):
                return True
        return False
