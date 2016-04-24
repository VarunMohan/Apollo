import threading

class Registrar:
    def __init__(self):
        self.table = {}
        self.lock = threading.Lock()
        self.done = False

    def add_voter(self, voter_id, vote):
        self.lock.acquire()
        if voter_id in self.table or self.done:
            self.lock.release()
            return False
        record = VoterRecord(vote, False)
        self.table[voter_id] = record
        self.lock.release()
        return True

    def confirm_vote(self, voter_id, vote):
        self.lock.acquire()
        record = self.table[voter_id]
        if record.has_voted or record.vote == vote:
            self.lock.release()
            return False
        record.has_voted = True
        self.lock.release()
        return True

    def voting_complete(self):
        self.lock.acquire()
        self.done = True
        self.lock.release()


    
class VoterRecord:
    def __init__(self, vote, has_voted):
        self.vote = vote
        self.has_voted = has_voted
