from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
import entity_locations
import sys
from voter import Voter

import pickle
from flask import Flask, render_template, request
from flaskext.xmlrpc import XMLRPCHandler, Fault

app = Flask(__name__)
r_endpoint = entity_locations.get_registrar_endpoint()
r = ClientRegistrar(r_endpoint)

@app.route('/api/submit_vote', methods=['POST'])
def submit_vote():
    e , tallier_endpoints = r.get_election(int(request.form['eid']))
    # can randomize this later
    t = ClientTallier(tallier_endpoints[0])
    voter = Voter(request.form['voter_id'], r, t, e)
    test = voter.vote(request.form['candidate'])
    return render_template('voting_interface.html')

@app.route('/')
def hello_world():
    return render_template('voting_interface.html')

if __name__ == '__main__':
    endpoint = entity_locations.get_voting_interface_endpoint()
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

