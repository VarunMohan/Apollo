class Registrar:
    def __init__(self):
        self.table = {}

    def add_voter(self, voter_id, vote):
        if voter_id in self.table:
            return False
        record = VoterRecord(vote, False)
        self.table[voter_id] = record
        return True

    def confirm_vote(self, voter_id, vote):
        if record.has_voted:
            return False
        record.has_voted = True
        return True

    
class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted
