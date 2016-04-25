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

If you get an error message that includes the following lines:
```
  Running setup.py install for Flask-XML-RPC
    Skipping installation of /afs/athena.mit.edu/user/r/s/rsridhar/Desktop/6.857/Apollo/apollo/env/lib/python3.4/site-packages/flaskext/__init__.py (namespace package)
      File "/afs/athena.mit.edu/user/r/s/rsridhar/Desktop/6.857/Apollo/apollo/env/lib/python3.4/site-packages/flaskext/xmlrpc.py", line 252
        except Fault, fault:
                    ^
    SyntaxError: invalid syntax
```

you need to use `2to3` to fix `xmlrpc.py` to work with python3:
```
2to3 -w env/lib/python3.4/site-packages/flaskext/xmlrpc.py
```

To deactivate:
```
deactivate
```

## Building
```
python aggregatetallier.py
python authority.py
python tallier.py 0
python tallier.py 1
python registrar.py
python main.py
```

This runs two talliers.

## TODO
* Distribute Tallier and don't hardcode port numbers
* Figure out why `app.debug = True` doesn't work
* Optimize crypto
* Pretty website templates
* Authenticate voters
* Unexpose API
* ZNP for end-to-end integrity check
* Client-side encryption of vote
