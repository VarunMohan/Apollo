from clientregistrar import ClientRegistrar
from clientauthority import ClientAuthority
from clienttallier import ClientTallier
from election import Election
from voter import Voter
import entitylocations

import random
import pickle


if __name__ == '__main__':
    NUM_VOTERS = 5
    NUM_CANDIDATES = 5
    FREQUENCY = 1

    a = ClientAuthority()
    r_endpoint = entitylocations.get_registrar_endpoint()
    r = ClientRegistrar(r_endpoint)
    e = r.get_election()
    eid = e.election_id
    t = ClientTallier()

    voters = [Voter(i, r, t, e) for i in range(NUM_VOTERS)]
    expected_vote_totals = {i:0 for i in range(NUM_CANDIDATES)}

    current_votes = 0
    for voter in voters:
        candidate = random.randint(0, NUM_CANDIDATES - 1)
        expected_vote_totals[candidate] += 1

        voter.vote(candidate)
        if current_votes % FREQUENCY == 0:
            print(current_votes)
        current_votes += 1

    result = a.compute_result(eid, t)
    real_vote_totals = e.decode_result(result)

    print('Expected: {}'.format(expected_vote_totals))
    print('Actual:   {}'.format(real_vote_totals))
    for i in range(NUM_CANDIDATES):
        assert expected_vote_totals[i] == real_vote_totals[i]

    print("Everything is going swimmingly")

