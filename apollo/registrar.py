import threading

class Registrar:
    def __init__(self):
        self.table = {}
        self.lock = threading.Lock()

    def add_voter(self, voter_id, vote):
        self.lock.acquire()
        if voter_id in self.table:
            self.lock.release()
            return False
        record = VoterRecord(vote, False)
        self.table[voter_id] = record
        self.lock.release()
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
