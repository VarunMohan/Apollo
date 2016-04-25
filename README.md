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
python aggregatetallier.py
python authority.py
python tallier.py 0
python tallier.py 1
python registrar.py
python main.py
```

This runs two talliers

