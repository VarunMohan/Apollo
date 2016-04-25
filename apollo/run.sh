#!/bin/bash

killall INT python
echo "Starting Aggregate Tallier"
python aggregate_tallier.py > logs/aggregate_tallier.log 2>&1 &
sleep 1
echo "Starting Authority"
python authority.py > logs/authority.log 2>&1 &
sleep 1
echo "Starting Tallier 0"
python tallier.py 0 > logs/tallier0.log 2>&1 &
sleep 1
echo "Starting Tallier 1"
python tallier.py 1 > logs/tallier1.log 2>&1 &
sleep 1
echo "Starting Registrar"
python registrar.py > logs/tallier2.log 2>&1 &
sleep 1
echo "Running Main"
python main.py
