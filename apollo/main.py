from tallier import Tallier
from registrar import Registrar
from authority import Authority, Election
from voter import Voter

import random

if __name__ == '__main__':
    NUM_VOTERS = 1000
    NUM_CANDIDATES = 16


    a = Authority()
    e = a.create_election(NUM_VOTERS, NUM_CANDIDATES)
    eid = e.election_id
    r = Registrar(e)
    t = Tallier(r, e)

    voters = [Voter(i, r, t, e) for i in range(NUM_VOTERS)]
    expected_vote_totals = {i:0 for i in range(NUM_CANDIDATES)}

    current_votes = 0
    for voter in voters:
        candidate = random.randint(0, NUM_CANDIDATES - 1)
        expected_vote_totals[candidate] += 1

        voter.vote(candidate)
        if current_votes % 10 == 0:
            print(current_votes)
        current_votes += 1

    result = a.compute_result(eid, t)
    real_vote_totals = e.decode_result(result)

    print('Expected: {}'.format(expected_vote_totals))
    print('Actual  : {}'.format(real_vote_totals))
    for i in range(NUM_CANDIDATES):
        assert expected_vote_totals[i] == real_vote_totals[i]

    print("Everything is going swimmingly")
