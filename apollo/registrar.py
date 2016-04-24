import threading

class Registrar:
    def __init__(self, election):
        self.election = election
        self.table = {}
        self.done = False

    def add_voter(self, voter_id, vote):
        if voter_id in self.table or self.done:
            return False
        record = VoterRecord(vote, False)
        self.table[voter_id] = record
        return True

    def confirm_vote(self, voter_id, vote):
        record = self.table[voter_id]
        if record.has_voted or record.vote != vote:
            return False
        record.has_voted = True
        return True

    def voting_complete(self):
        self.done = True



class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted
