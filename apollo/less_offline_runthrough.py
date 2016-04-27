from client_registrar import ClientRegistrar
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

    r_endpoint = entity_locations.get_registrar_endpoint()
    r = ClientRegistrar(r_endpoint)
    eid = r.register_election(voter_ids, candidates)
    print("Got Election ID", eid)
    if eid == False:
        print("Could not get an election")
        sys.exit(0)

    e, _ = r.get_election(eid)

    while r.is_election_running(eid):
        time.sleep(1)

    result = r.get_result(eid)
    real_vote_totals = e.decode_result(result)
    print(real_vote_totals)

    print("Everything is going swimmingly")

