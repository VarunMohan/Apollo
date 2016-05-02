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
2to3 -w env/lib/python3.x/site-packages/flaskext/xmlrpc.py
```
Note you will need to fill x with your appropriate version number.

To deactivate:
```
deactivate
```

## Building
Execute the following script to run the system with n talliers.

```
./run.sh n
```

There are now 4 ways to interact with the running system. The preferred is to use `localhost:7000` to create an election, and use `localhost:7777` to cast your votes.

Alternatively, `less-offline-runthrough.py` will create an election with preset candidates and voter ids. You must go to `localhost:7777` to cast your vote and end the election.

Running `demo.py` will start an election using pre-set candidates corresponding to the 2016 US Presidential Race, with a pre-set list of valid voter ids.

Finally, `offline-runthrough.py` will create an election and execute votes, requiring no website interaction.

## Debugging
* Add `sys.stdout.flush()` to see the output of stdout in logs

## TODO
* Optimize crypto (sunl)
* Error Handling (sunl)
* Malicious tests (sunl)
* ZNP for end-to-end integrity check (sunl)
* Client-side encryption of vote (kevinzhu)
* Unexposed API (vmohan, sunl)
* Written Report (kevinzhu)
