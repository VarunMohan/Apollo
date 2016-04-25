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

## Building
```
python authority.py
python tallier.py
python registrar.py
python main.py
```

TODO: Distribute Tallier and don't Hardcode Port Numbers
