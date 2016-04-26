from crypto import paillier
from crypto import znp
import Crypto.Util.number as pycrypto

class Voter:
    def __init__(self, voter_id, registrar, tallier, election):
        self.voter_id = voter_id
        self.registrar = registrar
        self.tallier = tallier
        self.election = election
        self.evote = None
        self.r = None
        self.proof = None

    def encrypt_vote(self, candidate):
        m = self.election.n_voters + 1
        # add one because of overflow case
        vote = pow((m), candidate)
        (self.evote, self.r) = paillier.encrypt(self.election.pk, vote)

        esum = pycrypto.getRandomInteger(1024) # in the future, the tallier sends this number

        u = []

        n = self.election.pk.n

        for i in range(self.election.n_candidates):
            newu = (self.evote * pycrypto.inverse(pow(self.election.pk.g, pow(m, i), n * n), n * n)) % (n * n)
            u.append(newu)

        self.proof = znp.gen_proof(self.election.pk, u, esum, candidate, self.r)
        
        #return paillier.encrypt(self.election.pk, vote)

    def vote(self, candidate):
        self.encrypt_vote(candidate)
        if self.registrar.add_voter(self.election.election_id, self.voter_id, self.evote):
            if self.tallier.send_vote(self.voter_id, self.evote, self.proof):
            # if self.tallier.send_vote(self.voter_id, encrypted_vote):
                return True
        return False
