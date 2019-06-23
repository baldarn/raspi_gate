#!/bin/bash

# check and restart flask app every 10 minutes
# */10 * * * * ./home/pi/raspi_gate/check_and_restart.sh

FLASK_APPS_RUNNING=$(ps aux | grep -c flask);

echo $FLASK_APPS_RUNNING

if [ $FLASK_APPS_RUNNING -eq 1 ]
then
    echo "start raspi gate!"
    cd /home/pi/raspi_gate
    . venv/bin/activate
    export FLASK_APP=raspi_gate
    export FLASK_ENV=production
    flask run --host=0.0.0.0 &
    echo "raspi gate started!"
fi
