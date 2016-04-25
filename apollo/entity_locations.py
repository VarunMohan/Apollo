def get_tallier_endpoints():
    endpoints = []
    with open('endpoints/talliers', 'r') as f:
        lines = f.readlines()
        for line in lines:
            endpoints.append(Endpoint(line))
    return endpoints


def get_authority_endpoint():
    with open('endpoints/authority', 'r') as f:
        line = f.readline()
        return Endpoint(line)

def get_registrar_endpoint():
    with open('endpoints/registrar', 'r') as f:
        line = f.readline()
        return Endpoint(line)

def get_aggregate_tallier_endpoint():
    with open('endpoints/aggregate_tallier', 'r') as f:
        line = f.readline()
        return Endpoint(line)

class Endpoint:
    def __init__(self, str_endpoint):
        endpoint = str_endpoint.strip().split(' ')
        self.hostname = endpoint[0]
        self.port = int(endpoint[1])

