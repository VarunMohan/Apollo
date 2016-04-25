# Apollo
A secure, anonymized voting system using the Paillier cryptosystem

## How to use `virtualenv`

Inside `apollo/`:
```
virtualenv env -p python3
```

To activate:
```
source env/bin/activate
pip install -e .
```

To deactivate:
```
deactivate
```

## Hack to make Flask-XML-RPC work with python3
```
2to3 -w env/lib/python3.4/site-packages/flaskext/xmlrpc.py
```

## Building
```
python authority.py
python tallier.py
python registrar.py
python main.py
```

## TODO
* Distribute Tallier and don't hardcode port numbers
* Figure out why `app.debug = True` doesn't work
* Optimize crypto
* Pretty website templates
* Authenticate voters
* Unexpose API
* ZNP for end-to-end integrity check
* Client-side encryption of vote
