from client_tallier import ClientTallier
from client_registrar import ClientRegistrar
from crypto import paillier
import entity_locations

import pickle
from flask import Flask
from flaskext.xmlrpc import XMLRPCHandler, Fault
from flask import render_template


class AggregateTallier:
    def __init__(self):
        self.elections = {}

    # coming from registrar
    def register_talliers(self, election_id, tallier_endpoints, registrar_endpoint, pk):
        self.elections[election_id] = (tallier_endpoints, registrar_endpoint, pk)
        return True

    # coming from authority
    def compute_aggregate_tally(self, election_id):
        if election_id not in self.elections:
            return False
        total = 1
        tallier_endpoints, registrar_endpoint, pk = self.elections[election_id]
        for endpoint in tallier_endpoints:
            t = ClientTallier(endpoint)
            local_tally = t.tally_votes(election_id)
            if (local_tally):
                total = paillier.add(pk, local_tally, total)
        return total

app = Flask(__name__)
handler = XMLRPCHandler('api')
handler.connect(app, '/api')
endpoint = entity_locations.get_authority_endpoint()
at = AggregateTallier()

@handler.register
def register_talliers(req):
    args = pickle.loads(req.data)
    return pickle.dumps(at.register_talliers(args['election_id'], args['tallier_endpoints'], args['registrar_endpoint'], args['pk']))

@handler.register
def compute_aggregate_tally(req):
    args = pickle.loads(req.data)
    return pickle.dumps(at.compute_aggregate_tally(args['election_id']))

@app.route('/')
def hello_world():
    return render_template('aggregate_tallier.html')

if __name__ == '__main__':
    endpoint = entity_locations.get_aggregate_tallier_endpoint()
    app.run(host=endpoint.hostname, port=endpoint.port, debug=True)

