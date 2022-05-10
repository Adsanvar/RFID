#!/bin/bash
# export FLASK_APP=~/Documents/RFID/api
# export FLASK_ENV=development
# export DEBUG=1
# export FLASK_RUN_PORT=5000
# flask run
# flask run --no-reload
# flask run -h 192.168.1.65

timer=15

echo "Application will start in: "
while (($timer !=0))
do
    echo $timer
    sleep 1s
    timer=$((timer-1))
done

python3 server.py
