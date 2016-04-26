from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
from client_tallier import ClientTallier
from election import Election
from voter import Voter
import entity_locations

import random
import pickle
import sys


if __name__ == '__main__':
    NUM_VOTERS = 5
    NUM_CANDIDATES = 2
    FREQUENCY = 1

    r_endpoint = entity_locations.get_registrar_endpoint()
    r = ClientRegistrar(r_endpoint)
    eid = r.register_election(NUM_VOTERS, NUM_CANDIDATES)
    print("Got Election ID", eid)
    if eid == False:
        print("Could not get an election")
        sys.exit(0)

    e, tallier_endpoints = r.get_election(eid)

    print("Connected to Talliers:")
    for endpoint in tallier_endpoints:
        print(endpoint.hostname, str(endpoint.port))

    voters = [Voter(i, r, ClientTallier(tallier_endpoints[i%len(tallier_endpoints)]), e) for i in range(NUM_VOTERS)]
    expected_vote_totals = {i:0 for i in range(NUM_CANDIDATES)}

    current_votes = 0
    for voter in voters:
        candidate = random.randint(0, NUM_CANDIDATES - 1)
        expected_vote_totals[candidate] += 1

        voter.vote(candidate)
        if current_votes % FREQUENCY == 0:
            print("Completed Processing Vote:", current_votes)
        current_votes += 1

    a = ClientAuthority()
    result = a.compute_result(eid)
    real_vote_totals = e.decode_result(result)

    print('Expected: {}'.format(expected_vote_totals))
    print('Actual:   {}'.format(real_vote_totals))
    for i in range(NUM_CANDIDATES):
        assert expected_vote_totals[i] == real_vote_totals[i]

    print("Everything is going swimmingly")

