from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from raspi_gate.auth import login_required
from raspi_gate.db import get_db

from time import sleep
import datetime
import requests

bp = Blueprint('gate', __name__)

LAST_OPEN_KEY = 'LAST_OPEN'
# salotto
LAST_UPDATE_SENSOR_KEY = 'LAST_UPDATE_SENSOR'
LAST_TEMPERATURE_IN_KEY = 'LAST_TEMPERATURE_IN'
LAST_TEMPERATURE_OUT_KEY = 'LAST_TEMPERATURE_OUT'
LAST_HUMIDITY_IN_KEY = 'LAST_HUMIDITY_IN'
LAST_HUMIDITY_OUT_KEY = 'LAST_HUMIDITY_OUT'
#studio
LAST_UPDATE_SENSOR_STUDIO_KEY = 'LAST_UPDATE_SENSOR_STUDIO'
LAST_TEMPERATURE_STUDIO_KEY = 'LAST_TEMPERATURE_STUDIO'
LAST_HUMIDITY_STUDIO_KEY = 'LAST_HUMIDITY_STUDIO'

GATE_OPEN_SECONDS = 50

@bp.route('/')
def index():
    """index page."""
    print(session.get(LAST_OPEN_KEY))
    last_open = session.get(LAST_OPEN_KEY)

    get_sensors()
    # salotto
    last_update_sensor = session.get(LAST_UPDATE_SENSOR_KEY)
    last_temperature_in = session.get(LAST_TEMPERATURE_IN_KEY)
    last_temperature_out = session.get(LAST_TEMPERATURE_OUT_KEY)
    last_humidity_in = session.get(LAST_HUMIDITY_IN_KEY)
    last_humidity_out = session.get(LAST_HUMIDITY_OUT_KEY)

    # studio
    last_update_sensor_studio = session.get(LAST_UPDATE_SENSOR_STUDIO_KEY)
    last_temperature_studio = session.get(LAST_TEMPERATURE_STUDIO_KEY)
    last_humidity_studio = session.get(LAST_HUMIDITY_STUDIO_KEY)

    is_open = False
    if last_open is not None:
        is_open = (datetime.datetime.now() - datetime.timedelta(seconds=GATE_OPEN_SECONDS)) < last_open

    return render_template(
        'gate/index.html', 
        is_open=is_open,
        last_update_sensor=last_update_sensor,
        last_temperature_in=last_temperature_in,
        last_temperature_out=last_temperature_out,
        last_humidity_in=last_humidity_in,
        last_humidity_out=last_humidity_out,
        last_update_sensor_studio=last_update_sensor_studio,
        last_temperature_studio=last_temperature_studio,
        last_humidity_studio=last_humidity_studio)


@bp.route('/open')
@login_required
def open():
    """Open the gate."""
    open_gate()
    return redirect(url_for('gate.index'))

def get_sensors():
    try:
        resp = requests.get(url='http://192.168.1.20', timeout=1)
        data = resp.json()

        print(data)

        session[LAST_UPDATE_SENSOR_KEY] = datetime.datetime.now()
        session[LAST_TEMPERATURE_IN_KEY] = data['temperature_in']
        session[LAST_TEMPERATURE_OUT_KEY] = data['temperature_out']
        session[LAST_HUMIDITY_IN_KEY] = data['humidity_in']
        session[LAST_HUMIDITY_OUT_KEY] = data['humidity_out']
    except Exception as e:
        print('sensor not reachable')

    try:
        resp = requests.get(url='http://192.168.1.21/temp', timeout=1)
        data = resp.json()

        print(data)

        session[LAST_UPDATE_SENSOR_STUDIO_KEY] = datetime.datetime.now()
        session[LAST_TEMPERATURE_STUDIO_KEY] = data['temperature']
        session[LAST_HUMIDITY_STUDIO_KEY] = data['humidity']
    except Exception as e:
        print('sensor not reachable')

def open_gate():
    try:
        resp = requests.get(url='http://192.168.1.21/gate', timeout=1)
        data = resp.json()
        print(data)
        session[LAST_OPEN_KEY] = datetime.datetime.now()
    except Exception as e:
        print('sensor not reachable')