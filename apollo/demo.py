from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
import entity_locations
from voter import Voter

import random
import json
from hashlib import sha256
from string import ascii_lowercase
from flask import Flask, render_template, request, session, redirect
from flaskext.xmlrpc import XMLRPCHandler, Fault

app = Flask(__name__)

r_endpoint = entity_locations.get_registrar_endpoint()
r = ClientRegistrar(r_endpoint)
voter_ids = ['rsridhar', 'kevinzhu', 'vmohan', 'sunl', 'akshayr']
candidates = ['clinton', 'cruz', 'kasich', 'sanders', 'trump']
eid = r.register_election(voter_ids, candidates)
e, tallier_endpoints = r.get_election(eid)
config = None

@app.route('/api/submit_vote', methods=['POST'])
def submit_vote():
    message = 'Success!'
    try:
        t = ClientTallier(random.choice(tallier_endpoints))
        voter = Voter(session['username'], r, t, e)
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
    if 'username' in session:
        if not r.is_election_running(eid):
            return render_template('demo_results.html', username = session['username'])
        else:
            return render_template('demo_interface.html', username = session['username'])
    elif 'email' in request.args:
        # coming back from auth.php (we think)
        email = request.args['email']
        token = request.args['token']
        name = request.args['name']

        key = session['key']
        secret = config['authSecret']
        to_hash = (email + key + secret).encode('utf-8')
        correct_token = sha256(to_hash).hexdigest()

        if token == correct_token:
            message = 'Success!'
            session['username'] = email[:-len('@mit.edu')]
        else:
            message = 'Authentication Failed'

        if not r.is_election_running(eid):
            return render_template('demo_results.html', username = session['username'])
        else:
            return render_template('demo_interface.html', username = session['username'])
    else:
        authURL = config['authURL']
        key = ''.join(random.choice(ascii_lowercase) for i in range(10))
        linkURL = authURL + '?key=' + key
        session['key'] = key
        return redirect(linkURL)

if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)

    app.secret_key = config['cookieSecret']
    app.run(host="localhost", port=8192, debug=False)
