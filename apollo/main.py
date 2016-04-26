from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
from client_tallier import ClientTallier
from election import Election
from voter import Voter
import entity_locations

import random
import pickle
import sys
import time


if __name__ == '__main__':
    voter_ids = ['rsridhar', 'kevinzhu', 'vmohan', 'sunl', 'akshayr']
    candidates = ['bernie', 'shillary']

    NUM_VOTERS = len(voter_ids)
    NUM_CANDIDATES = len(candidates)
    FREQUENCY = 1

    r_endpoint = entity_locations.get_registrar_endpoint()
    r = ClientRegistrar(r_endpoint)
    eid = r.register_election(voter_ids, candidates)
    print("Got Election ID", eid)
    if eid == False:
        print("Could not get an election")
        sys.exit(0)

    e, tallier_endpoints = r.get_election(eid)

    print("Connected to Talliers:")
    for endpoint in tallier_endpoints:
        print(endpoint.hostname, str(endpoint.port))

    a = ClientAuthority()
    while a.is_election_running(eid):
        time.sleep(1)

    result = a.get_result(eid)
    real_vote_totals = e.decode_result(result)
    print(real_vote_totals)

    print("Everything is going swimmingly")

