from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
from client_authority import ClientAuthority
import entity_locations
import sys
from voter import Voter

import pickle
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
    e , tallier_endpoints = r.get_election(int(request.form['eid']))
    # can randomize this later
    t = ClientTallier(tallier_endpoints[0])
    voter = Voter(request.form['voter_id'], r, t, e)
    test = voter.vote(request.form['candidate'])
    return render_template('voting_interface.html')

@app.route('/api/end_election', methods=['POST'])
def end_election():  
    a.compute_result(int(request.form['election_id']))
    return render_template('voting_interface.html')

    
@app.route('/')
def hello_world():
    return render_template('voting_interface.html')

if __name__ == '__main__':
    endpoint = entity_locations.get_voting_interface_endpoint()
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

