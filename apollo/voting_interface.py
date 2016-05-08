from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
import entity_locations
import sys
from voter import Voter

import pickle
import random
from flask import Flask, render_template, request
from flaskext.xmlrpc import XMLRPCHandler, Fault

app = Flask(__name__)
r_endpoint = entity_locations.get_registrar_endpoint()
# may want to remove the endpoint location
r = ClientRegistrar(r_endpoint)
a_endpoint = entity_locations.get_authority_endpoint()
a = ClientAuthority()

@app.route('/api/submit_vote', methods=['POST'])
def submit_vote():
    message = 'Success!'
    try:
        e , tallier_endpoints = r.get_election(int(request.form['eid']))
        if not e:
            message = 'Invalid Election ID'
            return render_template('voting_interface.html', submit_vote_msg = message)

        t = ClientTallier(random.choice(tallier_endpoints))
        voter = Voter(request.form['voter_id'], r, t, e)

        success = voter.vote(request.form['candidate'])
        if not success:
            message = 'Vote not cast: your vote was either invalid or already cast'
    except Exception:
        message = 'Something went wrong, please try again'

    return render_template('voting_interface.html', submit_vote_msg = message)



@app.route('/api/end_election', methods=['POST'])
def end_election():
    message = 'Success!'
    try:
        success = r.end_election(int(request.form['election_id']))
        if not success:
            message = 'Invalid Election ID'
    except ValueError:
        message = 'Election ID must be an integer'
    except Exception:
        message = 'Something went wrong, please try again'
    return render_template('voting_interface.html', end_election_msg = message)

@app.route('/')
def hello_world():
    election_ids = r.list_election_ids()
    if len(election_ids) > 0:
        e, _ = r.get_election(election_ids[0])
        candidates = e.candidates
        return render_template('voting_interface.html', election_ids = election_ids, candidates = candidates)
    else:
        return render_template('voting_interface.html', election_ids = election_ids)

if __name__ == '__main__':
    endpoint = entity_locations.get_voting_interface_endpoint()
    app.run(host=endpoint.hostname, port=endpoint.port, debug=False)

