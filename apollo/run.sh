#!/bin/bash

if [ -z "$1" ]; then
    #By default we have four talliers
    TALLIER_MAX=4
else
    TALLIER_MAX=$(($1-1))
fi

killall INT python > /dev/null 2>&1
echo "Starting Aggregate Tallier"
python aggregate_tallier.py > logs/aggregate_tallier.log 2>&1 &
sleep 1
echo "Starting Authority"
python authority.py > logs/authority.log 2>&1 &
sleep 1
echo "Starting Registrar"
python registrar.py > logs/registrar.log 2>&1 &
for i in $(eval echo {0..$TALLIER_MAX}); do
    sleep 1
    echo "Starting Tallier $i"
    python tallier.py $i > logs/tallier$i.log 2>&1 &
done
sleep 1
echo "Starting Voting Interface"
python voting_interface.py > logs/voting_interface.log 2>&1 &
sleep 1

# Note sleep is selected to make sure all servers are ready to listen on their ports (May need to increase/decrease duration)
