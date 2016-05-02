from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
import entity_locations
import sys
from voter import Voter

import pickle
import random
from flask import Flask, render_template, request, session, redirect
from flaskext.xmlrpc import XMLRPCHandler, Fault

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

r_endpoint = entity_locations.get_registrar_endpoint()
# may want to remove the endpoint location
r = ClientRegistrar(r_endpoint)
voter_ids = ['rsridhar', 'kevinzhu', 'vmohan', 'sunl', 'akshayr']
candidates = ['clinton', 'cruz', 'kasich', 'sanders', 'trump']
eid = r.register_election(voter_ids, candidates)
e, tallier_endpoints = r.get_election(eid)


@app.route('/api/submit_vote', methods=['POST'])
def submit_vote():
    message = 'Success!'
    try:
        t = ClientTallier(random.choice(tallier_endpoints))
        voter = Voter('rsridhar', r, t, e)
        success = voter.vote(request.form['candidate'])
        if not success:
            message = "Something went wrong, please try again"

    except Exception:
        message = 'Something went wrong, please try again'

    return message

@app.route('/api/end_election', methods=['POST'])
def end_election():
    message = 'Success!'
    try:
        success = r.end_election(eid)
        if not success:
            message = 'Invalid Election ID'
    except ValueError:
        message = 'Election ID must be an integer'
    except Exception:
        message = 'Something went wrong, please try again'

    return message




@app.route('/')
def hello_world():
    if r.is_election_running(eid):
        return render_template('demo_interface.html')
    else:
        return render_template('demo_results.html')

if __name__ == '__main__':
    app.run(host="localhost", port=8192, debug=False)
